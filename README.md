# ⏰ Tick Tock - Build Your Custom Pocket Watch

A beautiful platform for students to design and build custom pocket watches by combining PCB engineering, mechanical CAD design, and hands-on assembly. Built with Flask and featuring Hack Club authentication.

## 🎯 Overview

**Tick Tock** is a structured 7-hour hardware curriculum that bridges digital logic and physical craftsmanship. Students will:

1. **Schematic Design** (2 hours) - Design the watch's brain with component selection and power management
2. **PCB Layout** (2 hours) - Route traces and optimize for small-form-factor boards  
3. **Case Design (CAD)** (2 hours) - Create protective, aesthetic enclosures using 3D modeling
4. **Assembly & BOM** (1 hour) - Finalize documentation and preparation for manufacturing

Upon completion, students receive:
- ✅ Custom PCB manufactured and shipped
- ✅ Case 3D printed in their chosen filament color
- ✅ Component kit (quartz crystal, battery, buttons, display/hands)
- ✅ Recognition in the Tick Tock gallery

## 🛠 Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Authentication**: Hack Club OAuth 2.0
- **Database**: SQLite
- **Design**: Blueprint Aesthetic with glassmorphism effects

## 📁 Project Structure

```
ttt/
├── api/
│   ├── app.py              # Flask server & routes
│   ├── templates/
│   │   └── index.html      # Main website
│   └── static/
│       ├── style.css       # Blueprint aesthetic styles
│       ├── script.js       # Interactive features
│       └── flag-orpheus.top.png  # Hack Club logo
├── README.md               # This file
└── bills/                  # BOM documentation
```

## 🎨 Design System

The website uses a **Blueprint Aesthetic** inspired by engineering workbenches and dark-mode IDEs:

### Color Palette
- **Background**: Midnight Charcoal (#0f1115)
- **Accent**: Electric Copper (#d97706)
- **Text**: Light Gray (#e5e7eb)
- **Muted Text**: Medium Gray (#9ca3af)

### Key Features
- **Grid Background**: Subtle grid overlay creating a CAD workspace feel
- **Glassmorphism Cards**: Frosted glass effect with blur and transparency
- **Rotating Gear Animation**: Subtle background animation reinforcing the "watch" theme
- **Watch Face Progress Tracker**: Visual progress using animated watch hands
- **Maker's Journal**: Terminal-style journal entries for build reflections

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip or conda
- Hack Club OAuth credentials (Client ID & Secret)

### Installation

1. **Clone or navigate to the project**
```bash
cd ttt
```

2. **Set up environment variables**
Create a `.env` file in the `api` folder:
```env
FLASK_SECRET_KEY=your-secret-key-here
HACKCLUB_CLIENT_ID=your-client-id
HACKCLUB_CLIENT_SECRET=your-client-secret
DATABASE_PATH=/path/to/rsvp.db
```

3. **Install dependencies**
```bash
pip install flask authlib python-dotenv
```

4. **Run the Flask server**
```bash
cd api
python app.py
```

5. **Access the website**
Open your browser to `http://localhost:5000`

## 🔐 Hack Club Authentication

The website uses Hack Club's OAuth 2.0 integration. Users can:
- Login with their Hack Club account
- Track their build progress
- Keep a live Maker's Journal
- Submit projects for manufacturing

### Setting Up OAuth

1. Get OAuth credentials from [Hack Club's authentication portal](https://auth.hackclub.com)
2. Register your application with redirect URI: `http://localhost:5000/callback`
3. Add credentials to `.env` file

## 📝 Key Features

### For Students
- **Structured Curriculum**: Clear modules with time estimates and learning objectives
- **Progress Tracking**: Watch-face style progress indicator
- **Maker's Journal**: Document your build journey with timestamped entries
- **File Submission**: Upload Gerber files (PCB) and STL files (case design)
- **Gallery**: See previous student builds and Lapse videos

### For Organizers
- **Student Database**: Track progress across all participants
- **Build Analytics**: Monitor completion rates and bottlenecks
- **File Management**: Organize and verify submitted designs
- **Manufacturing Pipeline**: Prepare for PCB fabrication and 3D printing

## 🎬 Requirements

All students must follow two key rules:

1. **The Lapse Requirement**: Record all work using time-lapse software (Lapse, Hyperlapse, etc.)
   - Provides "proof of work" documentation
   - Creates engaging TikTok/Instagram content
   
2. **The Maker's Journal**: Keep 3–5 short entries (1–2 sentences each) reflecting on:
   - Challenges faced
   - Breakthroughs made
   - Design decisions

## 💻 Tools Recommended

- **Schematic & PCB**: KiCad (free & open-source)
- **CAD Design**: Fusion 360 (free for students) or Blender
- **Time-lapse**: Lapse app (iOS), Hyperlapse (Android), or Open Broadcaster Software (OBS)

## 🤝 Community

- **Join Slack**: #tick-tock channel on Hack Club Slack
- **Social Showcase**: Featured Lapse videos on Hack Club TikTok/Instagram
- **Custom Stickers**: Get meme-based stickers of your design!

## 📊 Database Schema

### builders Table
```sql
- id (INTEGER PRIMARY KEY)
- hc_id (TEXT UNIQUE) - Hack Club user ID
- slack_id (TEXT)
- name (TEXT)
- email (TEXT)
- watch_design (TEXT) - Design description
- schematic_status (TEXT) - not_started, in_progress, completed
- pcb_status (TEXT)
- cad_status (TEXT)
- assembly_status (TEXT)
- journal_entries (TEXT) - JSON array
- lapse_video_url (TEXT)
- verification_status (TEXT)
- timestamp (DATETIME)
```

## 🔧 Configuration

### Flask Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Home page |
| `/login` | GET | Hack Club OAuth login |
| `/callback` | GET | OAuth callback handler |
| `/logout` | GET | Logout user |
| `/api/journal` | POST | Add journal entry |
| `/api/progress` | GET | Get user progress |

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `FLASK_SECRET_KEY` | Session secret | random-string |
| `HACKCLUB_CLIENT_ID` | OAuth client ID | oauth_id_here |
| `HACKCLUB_CLIENT_SECRET` | OAuth secret | oauth_secret_here |
| `DATABASE_PATH` | SQLite DB location | /tmp/rsvp.db |

## 🎓 Curriculum Timeline

```
Week 1: Schematic Design (2 hours)
  ├─ Component selection
  ├─ Power management
  └─ First journal entry

Week 2: PCB Layout (2 hours)
  ├─ Footprint placement
  ├─ Trace routing
  └─ Design verification

Week 3: Case Design (2 hours)
  ├─ Template modification
  ├─ Custom exterior
  └─ 3D model export

Week 4: Assembly (1 hour)
  ├─ BOM finalization
  ├─ Documentation
  └─ Final submission
```

## 📸 Screenshots & Demo

See the live design inspiration in `readmecss.txt` for the full aesthetic vision.

## 🐛 Troubleshooting

### OAuth Login Not Working
- Verify Client ID/Secret are correct
- Check redirect URI matches Hack Club settings
- Clear browser cache and cookies

### Database Errors
- Ensure `DATABASE_PATH` directory exists and is writable
- Delete `rsvp.db` and restart to reinitialize

### CSS Not Loading
- Check Flask static folder path is correct
- Hard refresh browser (Ctrl+Shift+R)

## 📄 License

Built for the Hack Club community. Open source and free for educational use.

## 👋 Support

Questions or issues? Reach out to the Hack Club team or create an issue in the project repository.

---

**Built with ❤️ for makers by makers**
