# AgentGuard Prototype

Hackathon prototype for runtime governance of AI agent actions.

## Flow
User -> Login -> Dashboard -> File/Data -> Runtime Risk Engine -> Policy Engine -> Allow / Human Approval / Deny -> Audit Log

## Demo credentials
Email: admin@agentguard.local
Password: admin123

## Local backend
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000

## Local frontend
cd frontend
npm install
npm run dev

Open http://localhost:5173

## Demo buttons
Safe -> low risk -> allow
Approval -> medium risk -> human approval
Danger -> high risk -> deny
Injection -> prompt injection -> deny

## Supabase
Run database/schema.sql in Supabase SQL Editor, then set DATABASE_URL on Render.

## Vercel
Set VITE_API_URL to the deployed Render backend URL.

## Important
This is a hackathon prototype. The demo authentication is intentionally simple. Before production use, replace it with Supabase Auth, secure secret handling, object storage, row-level security, stronger policy controls, and sandboxed agent execution.
