# Milestones:
* This file shows all milestones considering the order and future planing of project and days we spent to get to that point.

### ① Core Web Monolith & Storage Pipeline: 
* Build the primary Web Backend (Flask API) and setup object storage.Auth & Database: Implement user sessions and database schema (PostgreSQL) to store user profiles, report records, and processing statuses (pending, processing, completed).Web Upload Pipeline: Build multi-part file upload endpoints handling images (PNG, JPEG), PDFs, and DICOM formats.Cloud Storage: Direct file streams straight to an Amazon S3 bucket (or local MinIO bucket for development) and save metadata to SQL.
### ②.Asynchronous Task Queue: Milestone 2.
* Set up the event broker so the web server doesn't freeze during heavy AI computation.Message Broker: Deploy Redis alongside Celery (Python's asynchronous task manager).Event Producer: Configure the Flask API to push an event (task_id, file_url) to the Redis queue immediately after a successful upload, returning a 202 Accepted response to the web browser.
### ③.AI & Explainability Microservice:
* Build the worker service that consumes queue messages and processes the medical files.Text Processing & Summary: Use a Medical VLM (e.g., LLaVA-Med or MedGemma) to parse reports or images and generate textual clinical summaries.Explainable Heatmap: Use pytorch-gradcam on medical vision models to generate the activation overlay (highlighting high-impact areas on X-rays).Output Sync: Save the generated summary and heatmap image back to S3, and update the SQL database record to completed.
### ④.Web Frontend & Real-Time Reporting UI:
* Develop the single-page web interface (React/Next.js or Flutter Web).Upload Dashboard: Build a drag-and-drop file upload zone for X-rays, PDFs, and DICOMs.Real-time Push Notifications: Implement Server-Sent Events (SSE) or WebSockets in Flask to push an alert to the browser the moment processing finishes.Interactive Viewer: Build a side-by-side comparison view allowing users to toggle between the original medical image, the AI-highlighted heatmap, and the generated summary.
### ⑤.Web Gateway & Production Deployment:
* Route web traffic securely and containerize the system.Reverse Proxy: Set up NGINX as the API Gateway/Load Balancer to handle incoming HTTPS web requests, route /api to Flask, and manage static frontend assets.Docker Containerization: Package the web frontend, Flask monolith, Redis broker, and PyTorch AI worker into Docker containers for easy deployment.
