
# 📽️ Movie Recommendation Backend

This is the backend service for a **Movie Recommendation System** built with Django, PostgreSQL, Redis, and DRF. It powers secure user authentication, personalized movie recommendations, and efficient movie search using the TMDb API.

---

## 🚀 Features

- 🔐 **JWT Authentication** – Secure login & signup
- 🎬 **Movie Management** – CRUD operations for movies and genres
- ⭐ **User Ratings** – Users can rate and review movies
- ❤️ **User Profiles** – Store preferences and profile data
- 🔎 **TMDb Integration** – Search for movies via the TMDb API
- ⚡ **Caching with Redis** – Optimized movie list retrieval
- 📚 **Interactive API Docs** – Swagger and ReDoc support
- 📊 **Personalized Recommendations** – Based on genre and user ratings

---

## 🧰 Tech Stack

| Layer       | Technology                         |
|-------------|-------------------------------------|
| Backend     | Django, Django REST Framework       |
| Auth        | JWT via `SimpleJWT`                 |
| Search API  | TMDb (The Movie Database) API       |
| Database    | PostgreSQL                          |
| Caching     | Redis                               |
| Docs        | Swagger (drf-yasg), ReDoc           |

---

## 📦 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/movie-recommendation-backend.git
cd movie-recommendation-backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file:
```env
DEBUG=True
SECRET_KEY=your_django_secret_key
DATABASE_URL=postgres://user:password@localhost:5432/moviedb
REDIS_URL=redis://localhost:6379
TMDB_API_KEY=your_tmdb_api_key
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Run Server
```bash
python manage.py runserver
```

---

## 📘 API Documentation

- Swagger: [`/swagger/`](http://localhost:8000/swagger/)
- ReDoc: [`/redoc/`](http://localhost:8000/redoc/)

---

## 🔐 Authentication

- **Signup:** `POST /api/signup/`
- **Login (JWT):** `POST /api/token/`
- **Refresh Token:** `POST /api/token/refresh/`

---

## 🔄 Endpoints Overview

| Endpoint              | Method | Description                                  |
|-----------------------|--------|----------------------------------------------|
| `/api/movies/`        | GET    | List all movies (cached)                     |
| `/api/genres/`        | GET    | List all genres                              |
| `/api/ratings/`       | POST   | Rate a movie                                 |
| `/api/profiles/`      | GET    | Get current user's profile                   |
| `/api/search/`        | GET    | Search TMDb for movies                       |
| `/api/search/`        | POST   | Add a new movie from search                  |
| `/api/recommend/`     | GET    | Get personalized movie recommendations       |

---

## 🔍 TMDb Movie Search Example

**GET** `/api/search/?q=inception`

**POST** `/api/search/`

```json
{
  "title": "Inception",
  "description": "A mind-bending thriller",
  "release_date": "2010-07-16",
  "duration": 148,
  "rating": 4.5,
  "genres": ["Sci-Fi", "Action"]
}
```

---

## 🧠 Recommendation Logic

- Recommends movies from **top-rated genres** by the user
- Falls back to **popular movies** (by average rating) if user has no ratings

---

## 🗃️ Project Structure

```
├── movies/
│   ├── models.py          # Models: Movie, Genre, Rating, UserProfile
│   ├── serializers.py     # Serializers for API data
│   ├── views.py           # All core logic & TMDb integration
│   ├── urls.py            # API routes via DRF router
├── config/
│   ├── urls.py            # Project-level routing + Swagger
├── requirements.txt
└── README.md              # You're here :)
```

---


## 📬 Contact

**Author:** Precious Nwaka  
📧 [preciousnwaka95@gmail.com](mailto:preciousnwaka95@gmail.com)
