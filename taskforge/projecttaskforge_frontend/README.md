# TaskForge frontend

React/Vite frontend for the TaskForge FastAPI backend.

## Run locally

```bash
npm install
npm run dev
```

Open the Vite URL shown in the terminal. The sign-in screen uses the same origin for the API by default; Vite proxies `/api/v1` requests to `http://127.0.0.1:8000`.

To use the frontend through ngrok, keep the backend running on port `8000`, start Vite on port `5173`, and forward the ngrok tunnel to `http://localhost:5173`. Leave the backend API address blank on the sign-in screen so API requests use the ngrok origin and the Vite proxy.

The UI uses the backend routes under `/api/v1`. Workspaces are loaded for the signed-in user from the backend and cached in this browser; project identifiers are saved locally because the backend does not expose a project list endpoint. Use **Mở bằng ID** to open a workspace manually, and the project ID field in the sidebar to open a project.
