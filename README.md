# 🐳 Three-Tier Docker Application

A modern, containerized three-tier web application demonstrating microservices architecture with Docker and Kubernetes support.

## 📋 Overview

This project showcases a complete three-tier architecture consisting of:

- **Frontend**: Static web interface served by Nginx
- **Backend**: RESTful API built with Python Flask
- **Database**: PostgreSQL database with persistent storage

The application demonstrates inter-service communication, health checks, and can be deployed using either Docker Compose or Kubernetes.

## 🏗️ Architecture

```
┌─────────────────┐
│    Frontend     │  (Nginx)
│   Port: 80      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Backend      │  (Python Flask)
│   Port: 5000    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Database     │  (PostgreSQL)
│   Port: 5432    │
└─────────────────┘
```

## 🛠️ Technology Stack

### Frontend
- **Nginx**: High-performance web server
- **HTML/CSS/JavaScript**: Static content with dynamic API calls

### Backend
- **Python 3.12**: Programming language
- **Flask 3.0.0**: Web framework
- **Flask-CORS**: Cross-Origin Resource Sharing support
- **Gunicorn**: WSGI HTTP Server
- **Psycopg2**: PostgreSQL adapter for Python

### Database
- **PostgreSQL**: Relational database
- **Sample Data**: Pre-populated messages table

## 📁 Project Structure

```
three-tier-app/
├── frontend/
│   ├── Dockerfile          # Nginx container configuration
│   ├── index.html          # Main frontend interface
│   └── nginx.conf          # Nginx configuration with API proxy
├── backend/
│   ├── Dockerfile          # Python Flask container configuration
│   ├── app.py             # Flask API application
│   └── requirements.txt    # Python dependencies
├── db/
│   ├── Dockerfile          # PostgreSQL container configuration
│   └── init.sql           # Database initialization script
├── k8s/
│   ├── frontend-deployment.yml    # Kubernetes frontend deployment
│   ├── frontend-service.yml       # Kubernetes frontend service
│   ├── backend-deployment.yml     # Kubernetes backend deployment
│   ├── backend-service.yml        # Kubernetes backend service
│   ├── database-deployment.yml    # Kubernetes database deployment
│   └── database-service.yml       # Kubernetes database service
└── docker-compose.yml      # Docker Compose configuration
```

## 🚀 Getting Started

### Prerequisites

#### For Docker Compose:
- Docker Engine (20.10 or later)
- Docker Compose (2.0 or later)

#### For Kubernetes:
- Kubernetes cluster (minikube, kind, or cloud provider)
- kubectl CLI tool
- Docker for building images

### 🐳 Deployment with Docker Compose

1. **Clone the repository**
   ```bash
   git clone https://github.com/MalakAlKazem/three-tier-app.git
   cd three-tier-app
   ```

2. **Start all services**
   ```bash
   docker-compose up -d
   ```

3. **Check service status**
   ```bash
   docker-compose ps
   ```

4. **View logs**
   ```bash
   # All services
   docker-compose logs -f
   
   # Specific service
   docker-compose logs -f backend
   ```

5. **Access the application**
   - Frontend: http://localhost
   - Backend API: http://localhost:5000
   - Database: localhost:5432

6. **Stop all services**
   ```bash
   docker-compose down
   ```

7. **Stop and remove volumes** (clean restart)
   ```bash
   docker-compose down -v
   ```

### ☸️ Deployment with Kubernetes

1. **Build Docker images**
   ```bash
   cd frontend && docker build -t three-tier-app-frontend:latest .
   cd ../backend && docker build -t three-tier-app-backend:latest .
   cd ../db && docker build -t three-tier-app-database:latest .
   cd ..
   ```

2. **Apply Kubernetes configurations**
   ```bash
   # Deploy database
   kubectl apply -f k8s/database-deployment.yml
   kubectl apply -f k8s/database-service.yml
   
   # Deploy backend
   kubectl apply -f k8s/backend-deployment.yml
   kubectl apply -f k8s/backend-service.yml
   
   # Deploy frontend
   kubectl apply -f k8s/frontend-deployment.yml
   kubectl apply -f k8s/frontend-service.yml
   ```

3. **Check deployment status**
   ```bash
   kubectl get pods
   kubectl get services
   ```

4. **Access the application**
   ```bash
   # Get the frontend service URL (minikube)
   minikube service frontend --url
   ```

5. **Clean up**
   ```bash
   kubectl delete -f k8s/
   ```

## 🔌 API Endpoints

### Base URL
- Docker Compose: `http://localhost:5000`
- Frontend proxy: `/api` (proxied through Nginx)

### Available Endpoints

#### `GET /`
Get API information and available endpoints.

**Response:**
```json
{
  "status": "healthy",
  "message": "Backend API is running!",
  "endpoints": {
    "/": "This help message",
    "/api/message": "Get the latest message from database",
    "/api/messages": "Get all messages from database",
    "/api/health": "Health check endpoint"
  }
}
```

#### `GET /api/message`
Retrieve the latest message from the database.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "text": "Hello from the database! This is a three-tier application.",
    "created_at": "2024-01-15T10:30:00"
  }
}
```

#### `GET /api/messages`
Retrieve all messages from the database.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 3,
      "text": "Python Flask is great for building APIs.",
      "created_at": "2024-01-15T10:30:02"
    },
    {
      "id": 2,
      "text": "Docker makes containerization easy!",
      "created_at": "2024-01-15T10:30:01"
    }
  ],
  "count": 2
}
```

#### `GET /api/health`
Check the health status of the backend and database connection.

**Response:**
```json
{
  "api": "healthy",
  "database": "healthy"
}
```

## 🔍 Health Checks

All services include health checks for monitoring:

- **Frontend**: `http://localhost/health`
- **Backend**: `http://localhost:5000/api/health`
- **Database**: PostgreSQL readiness check via `pg_isready`

## 🗄️ Database

### Connection Details (Docker Compose)
- Host: `database` (internal) or `localhost` (external)
- Port: `5432`
- Database: `appdb`
- User: `dbuser`
- Password: `password123`

### Schema
```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    text VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Sample Data
The database is pre-populated with sample messages on initialization.

## 🔧 Configuration

### Environment Variables

#### Backend
- `DB_HOST`: Database host (default: `database`)
- `DB_PORT`: Database port (default: `5432`)
- `DB_NAME`: Database name (default: `appdb`)
- `DB_USER`: Database user (default: `dbuser`)
- `DB_PASSWORD`: Database password (default: `password123`)

#### Database
- `POSTGRES_DB`: Database name
- `POSTGRES_USER`: Database user
- `POSTGRES_PASSWORD`: Database password

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using the port
   sudo lsof -i :80
   sudo lsof -i :5000
   sudo lsof -i :5432
   ```

2. **Database Connection Failed**
   - Ensure the database container is healthy: `docker-compose ps`
   - Check database logs: `docker-compose logs database`
   - Wait for database initialization (may take 10-30 seconds on first start)

3. **Frontend Can't Connect to Backend**
   - Verify backend is running: `docker-compose ps backend`
   - Check Nginx proxy configuration in `frontend/nginx.conf`
   - View frontend logs: `docker-compose logs frontend`

4. **Kubernetes Pods Not Starting**
   ```bash
   # Describe pod to see error details
   kubectl describe pod <pod-name>
   
   # Check pod logs
   kubectl logs <pod-name>
   ```

## 🧪 Testing

### Manual Testing

1. **Test Frontend**
   ```bash
   curl http://localhost
   ```

2. **Test Backend Directly**
   ```bash
   curl http://localhost:5000/api/health
   curl http://localhost:5000/api/message
   curl http://localhost:5000/api/messages
   ```

3. **Test Database Connection**
   ```bash
   docker-compose exec database psql -U dbuser -d appdb -c "SELECT * FROM messages;"
   ```

## 📝 Development

### Making Changes

1. **Frontend Changes**
   - Edit `frontend/index.html` or `frontend/nginx.conf`
   - Rebuild: `docker-compose up -d --build frontend`

2. **Backend Changes**
   - Edit `backend/app.py` or `backend/requirements.txt`
   - Rebuild: `docker-compose up -d --build backend`

3. **Database Schema Changes**
   - Edit `db/init.sql`
   - Rebuild with clean database: `docker-compose down -v && docker-compose up -d`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available for educational purposes.

## 👥 Author

MalakAlKazem

## 🙏 Acknowledgments

- Flask documentation
- Docker documentation
- PostgreSQL documentation
- Kubernetes documentation
