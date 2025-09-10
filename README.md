# szakacstas_llm_training

// Project overview and how to run

This repository contains two main parts:

- Backend: a FastAPI application located in `03_python_fastapi_project/src`. It provides a product management API (create/list/get/update/delete products) backed by SQLite via SQLAlchemy/aiosqlite. The API exposes interactive OpenAPI docs at `/docs` when running locally.
- UI: a modern frontend located in `05_design` that implements a product management interface using Vue 3 + TypeScript, Vite, and Tailwind CSS. The UI communicates with the FastAPI backend (expected at `http://localhost:8000` in development).

Summary of key endpoints (backend):

- `GET /` - welcome message
- `POST /products/` - create product
- `GET /products/` - list products
- `GET /products/{id}` - get a product
- `PUT /products/{id}` - update a product
- `DELETE /products/{id}` - delete a product

Where to find the code:

- Backend: `03_python_fastapi_project/src` (main FastAPI app is `main.py`)
- Frontend/UI: `05_design` (Vite + Vue app in `src/`)

Quick start (development)

1) Backend (FastAPI)

```bash
# change into backend folder
cd 03_python_fastapi_project/src

# (optional) install 'uv' if not present (project uses uv for env & scripts)
curl -LsSf https://astral.sh/uv/install.sh | sh

# install dependencies managed by uv
uv sync

# start FastAPI with autoreload
uv run uvicorn main:app --reload
```

The backend will be available at: http://localhost:8000
Open API docs: http://localhost:8000/docs

Notes:
- The project uses SQLite by default; the DB file (e.g. `products.db`) will be created automatically when the app runs.
- You can customize settings with a `.env` file in the backend folder (see `DATABASE_URL`, `APP_NAME`, `DEBUG`).

2) Frontend (UI)

```bash
# change into UI folder
cd 05_design

# install Node dependencies
npm install

# start development server
npm run dev
```

The development UI server usually starts at: http://localhost:5173

Make sure the backend is running before using the UI so API calls succeed.

Handling CORS

If you see CORS (Cross-Origin) errors in the browser when the UI calls the API, enable CORS in the FastAPI app. A minimal example to add into `03_python_fastapi_project/src/main.py`:

```py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Troubleshooting

- If the backend port (8000) is already used, pass `--port <PORT>` to `uv run uvicorn ...` and update the UI config if necessary.
- If the UI dev server chooses a different port, check its terminal output for the exact URL.
- If using a system-wide Python environment, prefer creating a virtualenv for the backend to isolate deps.

Try-it examples

Create a product (curl):

```bash
curl -X POST "http://localhost:8000/products/" \
  -H "Content-Type: application/json" \
  -d '{"name":"hat","price":10,"stock":5}'
```

List products (curl):

```bash
curl -X GET "http://localhost:8000/products/"
```

Requirements coverage

- Scan `03_python_fastapi_project/src/README.md` and `05_design/README.md` for UI and backend details: Done.
- Extend root `README.md` with general description about the UI and BE: Done.
- Add steps on how to start up and access the application: Done (backend and frontend startup steps included).

Next steps (optional):

- If you want, I can add a short `run-dev.sh` script at the repo root to start both servers concurrently, or add a minimal CORS change directly to the backend `main.py`.

Quickstart

```bash
# Start BE
(cd 03_python_fastapi_project/src && uv run uvicorn main:app --reload)

# Start UI
(cd 05_design && npm run dev)
```

