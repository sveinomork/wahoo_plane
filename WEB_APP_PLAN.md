### **Web Application Development Plan: Wahoo Workout Generator (FastAPI Backend)**

**Application Type:** Full-stack Web Application

**Core Technologies:**
*   **Frontend:** React (TypeScript)
*   **Styling:** Tailwind CSS
*   **Backend:** FastAPI (Python)
*   **Database:** (Optional, for saving user workouts and pre-defined sections) SQLite (for simplicity) or PostgreSQL (for scalability)
*   **Deployment:** Docker (for containerization)

**Design Principles (Modern & Nice Layout):**
*   Clean & Intuitive UI, Responsive Design, Visual Feedback, Accessibility, Modern Aesthetics.

---

#### **Phase 1: Planning & Setup (1-2 Days)**

1.  **Detailed Feature Specification:**
    *   Workout Creation:
        1.  **From YAML File (Upload):** User uploads a YAML file.
        2.  **From Pre-defined Sections (Library):** User selects and combines pre-defined interval sections.
        3.  **Interactive Builder:** User builds a workout step-by-step.
    *   Workout Display: All created workouts (regardless of method) should be displayed graphically.
    *   Workout Management:
        *   List all created workouts.
        *   View/Edit/Delete existing workouts.
        *   Download `.plan` file.
        *   Download PNG image.
    *   Workout Library: Pre-defined workout templates (interval sections).

2.  **Technology Deep Dive & Tooling Setup:**
    *   Initialize React project (e.g., Vite).
    *   Set up Tailwind CSS.
    *   Initialize FastAPI project.
    *   Configure TypeScript for frontend.
    *   Set up Git repository for the web app.

3.  **Basic Project Structure:**

    ```
    wahoo-web-app/
    ├── frontend/
    │   ├── public/
    │   ├── src/
    │   │   ├── components/
    │   │   ├── pages/
    │   │   ├── utils/
    │   │   ├── App.tsx
    │   │   ├── index.tsx
    │   │   └── tailwind.css
    │   ├── package.json
    │   └── tsconfig.json
    ├── backend/
    │   ├── app/             # FastAPI application code
    │   │   ├── api/         # API routers (e.g., workouts.py, interval_sections.py)
    │   │   ├── core/        # Core logic (e.g., python_processor.py, models.py)
    │   │   ├── data/        # Static data (e.g., interval_sections.json)
    │   │   ├── main.py      # FastAPI app instance
    │   │   └── __init__.py
    │   ├── requirements.txt # Python dependencies
    │   ├── .env             # Environment variables
    │   └── Dockerfile (for backend)
    ├── shared/ # Optional: for shared types/interfaces (e.g., Pydantic models for API)
    ├── .gitignore
    ├── Dockerfile (for overall app, if using multi-stage build)
    └── README.md
    ```

---

#### **Phase 2: Backend Development (FastAPI) (5-7 Days)**

This phase will focus on building the FastAPI backend, which will directly leverage your existing Python logic.

1.  **FastAPI Setup:**
    *   Install FastAPI and Uvicorn: `pip install fastapi uvicorn`
    *   Create `backend/app/main.py` for the FastAPI app instance.
    *   Configure CORS middleware in FastAPI.

2.  **Pydantic Models for Data Validation:**
    *   Define Pydantic models for the `Workout Data Structure` and `Interval Section` data. This provides automatic request/response validation and documentation.
    *   These models can be shared with the frontend (e.g., via `shared/` directory or by generating TypeScript types from Python).

3.  **Core Python Logic Integration:**
    *   **Direct Import:** Since the backend is now Python, you can directly import and call functions from your `wahoo_plane` package (`yaml_to_plan`, `plot_intervals`, `calculate_tss`, `expand_intervals`). This is a significant advantage over the Node.js approach, as it avoids `child_process` overhead and complexity.
    *   Ensure `wahoo_plane` is installed in the backend's Python environment (e.g., listed in `requirements.txt`).

4.  **API Endpoints Implementation:**

    *   **A. Generate Workout (Unified Endpoint):**
        *   **Purpose:** This will be the primary endpoint for generating workouts from all three methods (interactive builder, pre-defined sections, or internal YAML parsing).
        *   **Endpoint:** `POST /api/workouts/generate`
        *   **Request Body:** Pydantic model of the `Workout Data Structure`.
        *   **Logic:**
            *   Receive the `Workout Data Structure` JSON.
            *   Recalculate `duration`, `tss`, `if` using your Python functions for validation and consistency.
            *   Call `yaml_to_plan` to get `.plan` content.
            *   Call `plot_intervals` to get PNG data (in-memory, base64 encoded).
            *   Return the updated workout object, `planContent`, and `pngBase64`.
        *   **Response Body:** JSON containing the full workout object, `planContent`, and `pngBase64`.

    *   **B. Upload YAML File:**
        *   **Purpose:** Allows users to upload a YAML file directly.
        *   **Endpoint:** `POST /api/workouts/upload-yaml`
        *   **Request Body:** `UploadFile` (FastAPI's file upload type).
        *   **Logic:**
            *   Receive the uploaded YAML file.
            *   Read and parse the YAML content using `PyYAML`.
            *   Convert the parsed YAML into the `Workout Data Structure` Pydantic model.
            *   **Crucially, then call the `POST /api/workouts/generate` endpoint internally (or reuse its core logic) with this parsed data.** This ensures all generation goes through the same validation and processing pipeline.
        *   **Response Body:** Same as `POST /api/workouts/generate`.

    *   **C. Get All Available Interval Sections:**
        *   **Purpose:** Provide the frontend with a list of pre-defined interval sections.
        *   **Endpoint:** `GET /api/interval-sections`
        *   **Logic:**
            *   For initial implementation: Read from a static JSON file (e.g., `backend/app/data/interval_sections.json`).
            *   For future: Fetch from a database.
        *   **Response Body:** JSON array of `Interval Section` Pydantic models.

    *   **D. Get a Specific Interval Section (Optional):**
        *   **Endpoint:** `GET /api/interval-sections/{section_id}`
        *   **Logic:** Retrieve a specific section by ID from static file/database.

5.  **Error Handling:** Implement FastAPI's exception handling for validation errors, internal server errors, etc.

---

#### **Phase 3: Frontend Development (React + Tailwind CSS) (5-7 Days)**

This phase remains largely the same, but the API calls will now target the FastAPI backend.

1.  **Core Layout & Navigation:** Responsive design with Tailwind CSS.
2.  **Workout Creation Page (`/create`):**
    *   **Tabbed Interface:** Implement tabs for "Build Interactively," "Upload YAML," and "Select from Library."
    *   **"Build Interactively" Tab:** Forms for warm-up, blocks (with rest between repeats), cool-down.
    *   **"Upload YAML" Tab:** File input for YAML upload.
    *   **"Select from Library" Tab:**
        *   Fetch data from `GET /api/interval-sections`.
        *   Display sections (cards/list) with names, descriptions, and "Add" button.
        *   When "Add" is clicked, append the `sectionData` to the current interactive workout state.
    *   **Real-time Graphical Display:** Charting library (e.g., Chart.js) to visualize the current workout being built.
    *   **Unified Generation:** A single "Generate Workout" button that sends the current workout state (from any tab) to `POST /api/workouts/generate`.
3.  **Workout Management Pages:** (If using database for saving workouts).
4.  **Styling with Tailwind CSS:** Focus on modern aesthetics.

---

#### **Phase 4: Deployment & Refinement (2-3 Days)**

1.  **Dockerization:**
    *   `backend/Dockerfile`: For the FastAPI app.
    *   `frontend/Dockerfile`: For the React app (served by Nginx or similar).
    *   `docker-compose.yml`: To orchestrate both services.
2.  **Testing:** Unit, integration, E2E tests.
3.  **Performance Optimization.**
4.  **Documentation:** Update `README.md`, API docs (FastAPI generates OpenAPI/Swagger UI automatically).
