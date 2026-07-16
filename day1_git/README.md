# Flask Task Manager

A simple but real Flask app: add tasks, set priority (low/medium/high), mark
them done, delete them, and filter by status. Data is stored in a JSON file.
Includes a small JSON API endpoint at `/api/tasks`.

## Project structure

```
flask-task-manager/
├── app.py                 # Flask app (routes + logic)
├── requirements.txt        # Python dependencies
├── vercel.json              # Vercel deployment config
├── .gitignore
├── api/
│   └── index.py            # Entry point Vercel uses to serve the Flask app
├── templates/
│   ├── base.html
│   └── index.html
└── static/
    └── style.css
```

## 1. Run it locally

```bash
python -m venv venv
source venv/bin/activate      # on Windows Git Bash: source venv/Scripts/activate
pip install -r requirements.txt
python app.py
```

Visit http://127.0.0.1:5000

## 2. Commit to GitHub using Git Bash

From inside the `flask-task-manager` folder:

```bash
git init
git add .
git commit -m "Initial commit: Flask task manager app"
```

Create a new empty repo on GitHub (no README/license, so there's no
conflict), then:

```bash
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

Replace `<your-username>/<your-repo>` with your actual GitHub repo path.
If Git Bash asks for credentials, use your GitHub username and a
Personal Access Token (not your password) — GitHub no longer accepts
plain passwords over HTTPS.

## 3. Deploy to Vercel

**Option A — via Vercel dashboard (easiest):**
1. Go to https://vercel.com/new
2. Import the GitHub repo you just pushed.
3. Vercel should auto-detect it as a Python project because of
   `vercel.json`. Leave settings as default and click **Deploy**.

**Option B — via Vercel CLI:**
```bash
npm install -g vercel
vercel login
vercel        # first deploy (follow prompts)
vercel --prod # promote to production
```

## Notes on Vercel + this app

- Vercel's filesystem is read-only except `/tmp`, so `app.py` stores
  `tasks.json` in `/tmp` when the `VERCEL` environment variable is present
  (Vercel sets this automatically). That means task data will **not**
  persist between deployments/cold starts on Vercel — it's fine for a demo,
  but for real persistence you'd swap in a database (e.g. Postgres via
  Vercel Postgres, or any hosted DB) — happy to help wire that up if you want.
- Locally, tasks are saved in `tasks.json` right next to `app.py`.
