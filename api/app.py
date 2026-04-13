from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key')

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

    return redirect(url_for('index', rsvp='success'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))





if __name__ == '__main__':
    app.run(debug=True)
