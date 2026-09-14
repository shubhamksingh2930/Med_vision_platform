# Manual Testing Guide: MedVision (Integrated A & B Features)

This document provides a comprehensive, step-by-step guide for manually testing the fully integrated MedVision API. This covers Person A's FastAPI endpoints working seamlessly with Person B's PostgreSQL Database and MinIO Storage implementations. 

## 🚀 Prerequisites (What must be active)

Before executing any API tests, you must ensure your local development environment and background services are fully running. Open your terminal and verify the following are active:

1. **Docker Infrastructure (PostgreSQL & MinIO)**
   - MinIO and PostgreSQL must be running in the background.
   - Command: `docker-compose up -d`
   - Verification: Open `http://localhost:9001` to ensure MinIO is up.
2. **Python Virtual Environment**
   - You must have your python environment activated so the API has access to `fastapi`, `psycopg2`, and `boto3`.
   - Command (Mac/Linux): `source ../venv/bin/activate` 
   - Command (Windows): `..\venv\Scripts\activate`
3. **FastAPI Server**
   - The API server must be actively running and listening for requests.
   - Command: `uvicorn app.main:app --reload`
   - Verification: You should see `Uvicorn running on http://127.0.0.1:8000` in the terminal.

---

## 🧪 Comprehensive API Testing

All tests will be performed using the built-in Swagger UI.
1. Open your browser and navigate to: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Test 1: User Registration
**Goal**: Verify the API successfully creates a user in the PostgreSQL database using Alembic schemas.

1. **Locate**: Find `POST /api/v1/auth/register` and click **Try it out**.
2. **Input**: Enter a test payload in the Request Body:
   ```json
   {
     "email": "doctor@hospital.com",
     "password": "SecurePassword123!"
   }
   ```
3. **Action**: Click **Execute**.
4. **Expected Output**: A `201 Created` response.
   ```json
   {
     "id": "e2d319... (a UUID)",
     "email": "doctor@hospital.com",
     "created_at": "2026-07-25T..."
   }
   ```
5. **Verification**: This confirms Person A's hashing logic and routing successfully utilized Person B's `get_db` SQLAlchemy Session.

### Test 2: User Login & JWT Generation
**Goal**: Verify the API can read the PostgreSQL database, verify the password, and issue a secure token.

1. **Locate**: Find `POST /api/v1/auth/login` and click **Try it out**.
2. **Input**: 
   - `username`: `doctor@hospital.com`
   - `password`: `SecurePassword123!`
3. **Action**: Click **Execute**.
4. **Expected Output**: A `200 OK` response.
   ```json
   {
     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
     "token_type": "bearer"
   }
   ```
5. **Authorization Step**: 
   - Copy the `access_token` string (without quotes).
   - Scroll to the very top of the Swagger page and click the green **Authorize** button.
   - Paste the token into the `value` field and click **Authorize**, then **Close**. All subsequent requests are now securely authenticated.

### Test 3: Get Current User Profile
**Goal**: Verify the API correctly decodes the JWT token and fetches the user from the database.

1. **Locate**: Find `GET /api/v1/auth/me` and click **Try it out**.
2. **Action**: Click **Execute** (No inputs required, it uses your Authorize token).
3. **Expected Output**: A `200 OK` response matching your registration details.
   ```json
   {
     "id": "e2d319... (a UUID)",
     "email": "doctor@hospital.com",
     "created_at": "2026-07-25T..."
   }
   ```

### Test 4: File Upload (Integration with MinIO & PostgreSQL)
**Goal**: Verify the API streams binary file data to MinIO using `boto3` and logs the metadata to PostgreSQL.

1. **Locate**: Find `POST /api/v1/upload/` and click **Try it out**.
2. **Input**: 
   - Click **Choose File** and select any image (e.g., a `.png` or `.jpg`) from your computer.
3. **Action**: Click **Execute**.
4. **Expected Output**: A `201 Created` response containing the storage paths.
   ```json
   {
     "id": "abcd12...",
     "original_filename": "chest_xray.png",
     "mime_type": "image/png",
     "file_size_bytes": "1048576",
     "r2_image_key": "raw_images/<user_id>/<file_id>.png",
     "r2_log_key": "logs/<user_id>/<file_id>_audit.json",
     "heatmap_image_url": null,
     "prediction_result": null,
     "status": "pending",
     "created_at": "2026-07-25T..."
   }
   ```
5. **Deep Verification**: 
   - **PostgreSQL**: The API successfully inserted this metadata into Person B's `MedicalRecord` table.
   - **MinIO**: Open `http://localhost:9001`, log in with `minioadmin`, and navigate to `med-vision-bucket`. You will see your image safely stored in the `raw_images/` folder, proving Person A successfully utilized Person B's storage wrapper.

### Test 5: List All Uploads
**Goal**: Verify the API can fetch multiple records tied to the authenticated user from the database.

1. **Locate**: Find `GET /api/v1/upload/` and click **Try it out**.
2. **Action**: Click **Execute**.
3. **Expected Output**: A `200 OK` response returning pagination data and a list of your files.
   ```json
   {
     "items": [
       {
         "id": "abcd12...",
         "original_filename": "chest_xray.png",
         ...
       }
     ],
     "total": 1,
     "page": 1,
     "size": 50
   }
   ```

### Test 6: Get Specific Upload Record
**Goal**: Verify the API can fetch a single specific record from the database.

1. **Locate**: Find `GET /api/v1/upload/{record_id}` and click **Try it out**.
2. **Input**: Paste the `id` you received from Test 4 into the `record_id` field.
3. **Action**: Click **Execute**.
4. **Expected Output**: A `200 OK` response returning the exact JSON metadata for that single file.
