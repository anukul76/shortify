# Shortify
FastAPI URL Shortener with Subscription Model
A production-ready URL Shortener built using FastAPI, featuring:

- Short link generation with analytics. 
- Role-based subscription plans (Free, Premium, Enterprise). 
- Rate limiting & usage quota per plan.
- Authentication & authorization with JWT.
- Async background tasks for logging and analytics.

### ⚡ Features
Shorten URLs – Generate unique short links with redirects.

- Subscription Plans – 
  - Free: Limited URLs, basic analytics. 
  - Premium: Higher limits, advanced analytics.
  - Enterprise: Custom plan, SLA support.

- User Authentication – JWT-based auth with role & plan enforcement.
- Usage Limits – Requests capped per plan with rate-limiting.
- Analytics – Track click counts, referrers, and geolocation (optional).
- Admin Panel – Manage users, plans, and quotas.

### 🛠️ Tech Stack
- Backend: FastAPI (async, high-performance).
- Database: PostgreSQL (URL & user storage), Redis (caching & rate limits).
- ORM: SQLAlchemy + Alembic for migrations. 
- Auth: JWT + OAuth2 Password Flow. 
- Task Queue (optional): Kafka/ Celery + Redis for async logging & analytics.
- Deployment: Docker + Uvicorn + Nginx.


## 🚀 Getting Started
1. Clone Repository
```
git clone https://github.com/yourusername/fastapi-url-shortener.git
cd fastapi-url-shortener
```
2. Setup Environment
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Run with Docker (Recommended)
```
docker-compose up --build
```
4. Database Migration
```
alembic upgrade head
```
5. Run Application

```
uvicorn app.main:app --reload
```
