from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
from dotenv import load_dotenv
import sqlite3
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key')
DATABASE = 'rsvp.db'

oauth = OAuth(app)
oauth.register(
    name='hackclub',
    server_metadata_url='https://auth.hackclub.com/.well-known/openid-configuration',
    client_id=os.environ.get('HACKCLUB_CLIENT_ID'),
    client_secret=os.environ.get('HACKCLUB_CLIENT_SECRET'),
    client_kwargs={
        'scope': 'openid profile email verification_status slack_id'
    }
)

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS rsvps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hc_id TEXT,
            slack_id TEXT,
            name TEXT,
            email TEXT,
            project_idea TEXT,
            project_type TEXT,
            verification_status TEXT,
            ysws_eligible INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    existing_cols = {row['name'] for row in db.execute('PRAGMA table_info(rsvps)')}
    columns = {
        'hc_id': 'TEXT',
        'slack_id': 'TEXT',
        'name': 'TEXT',
        'email': 'TEXT',
        'project_idea': 'TEXT',
        'project_type': 'TEXT',
        'verification_status': 'TEXT',
        'ysws_eligible': 'INTEGER'
    }

    for col, col_type in columns.items():
        if col not in existing_cols:
            db.execute(f'ALTER TABLE rsvps ADD COLUMN {col} {col_type}')

    db.commit()
    db.close()

@app.route('/')
def index():
    user = session.get('user')
    rsvp_status = request.args.get('rsvp')
    return render_template('index.html', user=user, rsvp_status=rsvp_status)

@app.route('/login')
def login():
    redirect_uri = url_for('auth_callback', _external=True)
    nonce = generate_token(32)
    session['oidc_nonce'] = nonce
    return oauth.hackclub.authorize_redirect(redirect_uri, nonce=nonce)

@app.route('/auth/callback')
def auth_callback():
    token = oauth.hackclub.authorize_access_token()
    nonce = session.pop('oidc_nonce', None)
    userinfo = oauth.hackclub.parse_id_token(token, nonce=nonce)

    session['user'] = {
        'hc_id': userinfo.get('sub'),
        'name': userinfo.get('name'),
        'email': userinfo.get('email'),
        'slack_id': userinfo.get('slack_id'),
        'verification_status': userinfo.get('verification_status'),
        'ysws_eligible': userinfo.get('ysws_eligible')
    }

    ensure_rsvp(session['user'])
    return redirect(url_for('index', rsvp='success'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def ensure_rsvp(user):
    if not user or not user.get('hc_id'):
        return

    db = get_db()
    existing = db.execute('SELECT id FROM rsvps WHERE hc_id = ?', (user['hc_id'],)).fetchone()
    if not existing:
        db.execute('''
            INSERT INTO rsvps (hc_id, slack_id, name, email, project_type, verification_status, ysws_eligible)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            user.get('hc_id'),
            user.get('slack_id'),
            user.get('name'),
            user.get('email'),
            'unspecified',
            user.get('verification_status'),
            1 if user.get('ysws_eligible') else 0
        ))
        db.commit()
    db.close()

@app.route('/api/rsvp', methods=['POST'])
def submit_rsvp():
    try:
        data = request.json
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        project_idea = data.get('project_idea', '').strip()
        project_type = data.get('project_type', '').strip()
        
        if not name or not email or not project_type:
            return jsonify({'error': 'Missing required fields'}), 400
        
        db = get_db()
        db.execute('''
            INSERT INTO rsvps (name, email, project_idea, project_type)
            VALUES (?, ?, ?, ?)
        ''', (name, email, project_idea, project_type))
        db.commit()
        db.close()
        
        return jsonify({'success': True, 'message': 'RSVP submitted successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def stats():
    try:
        db = get_db()
        total = db.execute('SELECT COUNT(*) FROM rsvps').fetchone()[0]
        physical = db.execute("SELECT COUNT(*) FROM rsvps WHERE project_type = 'physical'").fetchone()[0]
        software = db.execute("SELECT COUNT(*) FROM rsvps WHERE project_type = 'software'").fetchone()[0]
        db.close()
        
        return jsonify({
            'total': total,
            'physical': physical,
            'software': software
        })
    except:
        return jsonify({'total': 0, 'physical': 0, 'software': 0})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
