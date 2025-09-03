# -----------------------------
# 1. Frontend build (React + Vite)
# -----------------------------
    FROM node:18-alpine AS frontend-builder

    WORKDIR /app/frontend
    
    COPY frontend/package*.json ./
    RUN npm install --production
    
    COPY frontend/ .
    RUN npm run build
    
    
    # -----------------------------
    # 2. Backend (FastAPI + Python)
    # -----------------------------
    FROM python:3.11-slim AS backend
    
    WORKDIR /app
    
    RUN apt-get update && apt-get install -y --no-install-recommends build-essential && \
        rm -rf /var/lib/apt/lists/*
    
    # Install requirements
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    
    # Copy backend code
    COPY . .
    
    # Copy built frontend from stage 1
    COPY --from=frontend-builder /app/frontend/dist ./frontend/dist
    
    # Railway sets $PORT automatically
    CMD ["sh", "-c", "uvicorn run:app --host 0.0.0.0 --port ${PORT}"]
    