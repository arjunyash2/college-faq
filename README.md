# College FAQ Chatbot MVP

React + FastAPI + Gemini + local FAQ JSON. No login, database, or agent.

## Requirements
Python 3.10+ and Node.js 20+. Obtain a Gemini API key from Google AI Studio.

## Milestone 1: Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env # Windows: copy .env.example .env
```
Edit `backend/.env` with your real `GEMINI_API_KEY`. Sample FAQs are in `backend/data/faqs.json`; replace with verified college content before public use.

## Milestone 2: Backend
From `backend/`:
```bash
uvicorn app.main:app --reload
```
API docs: http://localhost:8000/docs

Test with:
```bash
curl -X POST http://localhost:8000/chat -H 'Content-Type: application/json' -d '{"message":"How do I apply for admission?"}'
```

Example response shape:
```json
{"answer":"Apply using the official college admissions portal.","sources":[{"id":"FAQ-001","question":"How do I apply for admission?"}]}
```
The example is illustrative; Gemini wording can vary.

## Milestone 3: Frontend
In a separate terminal:
```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```
Open http://localhost:5173. `VITE_API_URL` points to the backend origin.

## Milestone 4: Automated tests
From `backend/`:
```bash
pytest -q
```
Five tests cover health, blank input, oversized input, unknown fallback and source IDs. The Gemini call is mocked in the citation test, so tests need no API key.

## Milestone 5: Deployment
1. Push the project to GitHub, excluding `.env`.
2. On Render, deploy the backend using `render.yaml` or create a Python web service with root directory `backend`, build command `pip install -r requirements.txt`, and start command `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
3. Set `GEMINI_API_KEY` in Render's secret environment variables. Set `FRONTEND_ORIGIN` to the final frontend URL (no trailing slash).
4. On Vercel, import the same repository with root directory `frontend`, framework Vite, build command `npm run build`, output directory `dist`.
5. Set `VITE_API_URL` to the Render HTTPS backend URL and redeploy the frontend. Update `FRONTEND_ORIGIN` on Render to the Vercel HTTPS URL.
6. Verify `/health`, submit a known FAQ, test an unknown question, and check browser developer tools for CORS errors.

## API contract
`POST /chat` takes `{ "message": "..." }` (1–1000 characters, nonblank) and returns `{ "answer": "...", "sources": [{ "id": "FAQ-001", "question": "..." }] }`. Invalid input returns 422; upstream Gemini failures return 503.

## Security and limitations
The Gemini key is never exposed to React. FAQ IDs come from server-side retrieval, not Gemini. Keyword retrieval is intentionally basic: matching words do not prove relevance, and Gemini answers are not automatically fact-checked. For production, add stronger retrieval relevance checks, rate limiting, logging without personal data, abuse controls, and verified FAQ ownership. CORS is not authentication or rate limiting. The MVP does not guarantee that every generated claim is supported by cited entries.
