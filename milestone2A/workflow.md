# MedVision Workflow & Testing Guide (Milestone 1 & 2)

This document outlines the complete workflow of the MedVision platform up to **Milestone 2 (Person A's Integration)**, and provides instructions on how to test the new Asynchronous Processing (Celery/Redis) integration alongside our Milestone 1 infrastructure.

---

## 🏗️ 1. Architecture Overview (The Pipeline)

Our system is structured as a robust, industry-standard machine learning engineering pipeline. Here is the flow of data:

1. **Authentication (Person A + B)**
   - The user registers and logs in via FastAPI.
   - The API hashes the password and uses Person B's SQLAlchemy session to store the user in **PostgreSQL**.
   - A JWT Bearer token is returned to the user for secure API access.
2. **File Upload (Person A + B)**
   - The user uploads a medical image (PNG/JPG) or report (PDF/DICOM).
   - The API validates the file type and size.
   - Using Person B's storage wrapper (boto3), the API streams the raw file directly into **MinIO (S3)**.
   - An audit log (JSON) is generated and stored in MinIO.
   - A `MedicalRecord` entry is saved to **PostgreSQL** with a status of `PENDING`.
3. **Asynchronous Processing (Person A's Milestone 2)**
   - **[NEW]** Immediately after saving to the database, FastAPI acts as a **Producer**.
   - It enqueues a `process_medical_record_task` message containing the `record_id` into a **Redis Broker**.
   - The API immediately returns a `201 Created` response to the user, without waiting for the ML model to finish.
4. **Worker Execution (Person B's upcoming Milestone 2 work)**
   - *Note: This piece is not yet implemented.* Person B will build the Celery Worker that listens to the Redis queue, downloads the file from MinIO, processes it (or mocks it), and updates the PostgreSQL status to `COMPLETED`.

---

## 🚀 2. Testing the New Workflow

To test Person A's new Milestone 2 work, you will need to run Redis alongside our existing infrastructure.

### Step 2.1: Start the Infrastructure Services
Open your terminal and ensure all background services are running:
1. **PostgreSQL & MinIO**: 
   ```bash
   cd med_vision_backend
   docker-compose up -d
   ```
2. **[NEW] Redis Broker**:
   Start a local Redis container in the background to handle our Celery queues.
   ```bash
   docker run -d -p 6379:6379 --name medvision_redis redis
   ```

### Step 2.2: Start the FastAPI Server
Activate your virtual environment and start the API:
```bash
source venv/bin/activate
cd med_vision_backend
uvicorn app.main:app --reload
```

### Step 2.3: Verify the Producer (FastAPI -> Redis)
1. Open the Swagger UI at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
2. Authenticate by logging in (use the green **Authorize** button).
3. Execute the `POST /api/v1/upload/` endpoint and upload a medical image.
4. You should receive a fast `201 Created` response, exactly like Milestone 1.

**How do we know the new Celery/Redis integration worked?**
Because Person B hasn't built the worker yet, the task is currently sitting patiently inside the Redis queue! We can peek inside Redis to verify Person A's work:

1. Open your terminal and connect to the Redis container:
   ```bash
   docker exec -it medvision_redis redis-cli
   ```
2. Check the keys inside Redis:
   ```bash
   127.0.0.1:6379> keys *
   ```
3. You will see a celery queue key (e.g., `main-queue` or `celery`). You can inspect its length:
   ```bash
   127.0.0.1:6379> LLEN celery
   ```
   *If the number is greater than 0, Person A's FastAPI successfully enqueued the job for Person B's worker!*

---

## 🛠️ Next Steps
The integration for Person A's Milestone 2 is complete. The boundary is strictly maintained: FastAPI produces the job, and Redis holds it. 

The next step is for Person B to implement the Celery Worker script that connects to Redis, consumes the `process_medical_record_task`, and updates the database statuses (`PROCESSING` -> `COMPLETED`).
