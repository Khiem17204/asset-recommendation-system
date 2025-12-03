# Docker Setup Guide

This guide explains how to run the entire Asset Recommendation System (including the Angular UI) using Docker Compose.

## Quick Start

1. **Start all services:**
   ```bash
   docker-compose up --build -d
   ```

2. **Load foundational data:**
   ```bash
   python3 FAR-Trans/script.py
   ```

3. **Access the UI:**
   - Open your browser and navigate to: `http://localhost:4200`
   - The API is available at: `http://localhost:8000`

## Services

The Docker Compose setup includes:

1. **PostgreSQL Database** (`db`)
   - Port: `5432`
   - Database: `asset_recommendation`
   - User: `admin` / Password: `123`

2. **FastAPI Server** (`server`)
   - Port: `8000`
   - API Documentation: `http://localhost:8000/docs`

3. **Kafka** (`kafka`)
   - Port: `9092`

4. **Kafka Worker** (`worker`)
   - Processes recommendation requests
   - Automatically retrains models every 10 minutes

5. **Angular UI** (`ui`)
   - Port: `4200`
   - Served via nginx
   - Connects to API at `http://localhost:8000`

## Architecture

```
┌─────────────┐
│   Browser   │
│  (Port 4200)│
└──────┬──────┘
       │
       ▼
┌─────────────┐      ┌─────────────┐
│ Angular UI  │─────▶│ FastAPI     │
│  (nginx)    │      │  (Port 8000) │
└─────────────┘      └──────┬───────┘
                            │
                ┌───────────┼───────────┐
                ▼           ▼           ▼
         ┌──────────┐  ┌─────────┐  ┌──────────┐
         │PostgreSQL│  │  Kafka  │  │  Worker  │
         │(Port 5432)│  │(Port 9092)│ │          │
         └──────────┘  └─────────┘  └──────────┘
```

## Useful Commands

### View all running containers:
```bash
docker-compose ps
```

### View logs:
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f ui
docker-compose logs -f server
docker-compose logs -f worker
```

### Restart a specific service:
```bash
docker-compose restart ui
docker-compose restart server
docker-compose restart worker
```

### Stop all services:
```bash
docker-compose down
```

### Stop and remove volumes (⚠️ deletes data):
```bash
docker-compose down -v
```

### Rebuild a specific service:
```bash
docker-compose build ui
docker-compose up -d ui
```

## Development Workflow

### Making Changes to the UI

1. **Edit files in `ui/` directory**
2. **Rebuild the UI container:**
   ```bash
   docker-compose build ui
   docker-compose up -d ui
   ```

### Making Changes to the Backend

1. **Edit files in `server/` or `kafka_worker/` directories**
2. **Rebuild and restart:**
   ```bash
   docker-compose build server worker
   docker-compose up -d server worker
   ```

## Troubleshooting

### UI not loading
- Check if the container is running: `docker-compose ps`
- Check logs: `docker-compose logs ui`
- Verify port 4200 is not in use by another application

### API connection errors
- Ensure the server container is running: `docker-compose ps`
- Check server logs: `docker-compose logs server`
- Verify CORS is enabled (should be automatic with the latest code)

### Database connection issues
- Wait a few seconds after starting containers for PostgreSQL to initialize
- Check database logs: `docker-compose logs db`
- Verify the database volume exists: `docker volume ls`

### Worker not processing recommendations
- Check worker logs: `docker-compose logs worker`
- Ensure Kafka is running: `docker-compose ps kafka`
- Verify data is loaded: Check database or run the data loading script

## Environment Variables

You can customize the setup by modifying environment variables in `docker-compose.yml`:

- **Database credentials**: `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`
- **API URL**: The UI uses `http://localhost:8000` by default (configured in `ui/src/environments/environment.prod.ts`)

## Production Considerations

For production deployment:

1. **Change CORS origins** in `server/server.py` from `["*"]` to specific domains
2. **Use environment variables** for sensitive credentials
3. **Enable HTTPS** for both UI and API
4. **Use a reverse proxy** (nginx/traefik) in front of services
5. **Set up proper logging** and monitoring
6. **Configure database backups**

## Port Summary

| Service | Port | URL |
|---------|------|-----|
| Angular UI | 4200 | http://localhost:4200 |
| FastAPI Server | 8000 | http://localhost:8000 |
| PostgreSQL | 5432 | localhost:5432 |
| Kafka | 9092 | localhost:9092 |

