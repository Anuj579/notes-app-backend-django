
# Notes App - Backend (Django + DRF)

This is the **Django backend** for the Notes App project, providing APIs for the frontend to manage user authentication, profiles, and CRUD operations for notes. Built with **Django Rest Framework (DRF)** and deployed on **Render**.

---

## 🌟 Features
- **User Authentication**: Token-based authentication (JWT).
- **CRUD Operations**: Endpoints to create, read, update, and delete notes.
- **Profile Management**: Users can update their profile information and profile picture.
- **Account Deletion**: Users can delete their account if they choose to.
- **PostgreSQL Database**: Deployed using PostgreSQL for better scalability.
- **CORS Configured**: For seamless communication with the React frontend.

## 🚀 Getting Started

### Prerequisites
- Python 3.x installed on your system.
- A Supabase account for managing the PostgreSQL database (or any other cloud-hosted PostgreSQL database).

### Installation
```bash
# Clone the repository
git clone https://github.com/Anuj579/notes-app-backend-django.git
cd notes-app-backend-django

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
```

### 🛠️ Environment Variables

In the `.env` file, you need to set the following variables. Replace placeholders with your actual values:

```
DATABASE_URL=postgresql://<username>:<password>@<hostname>:<port>/<dbname>
CLOUDINARY_URL=cloudinary://<api_key>:<api_secret>@<cloud_name>
ALLOWED_HOSTS=your_backend_url,127.0.0.1,localhost,frontend_deployment_url
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

**Note**: Never hardcode sensitive information like database credentials or API keys directly in your code. Use environment variables instead.

### Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Run the Server
```bash
python manage.py runserver
```

## 📖 API Documentation

| Method   | Endpoint                 | Description                               |
|----------|--------------------------|-------------------------------------------|
| **POST** | `/register/`            | Register a new user                       |
| **POST** | `/login/`               | Log in a user                             |
| **POST** | `/token/refresh/`       | Refresh the JWT access token              |
| **GET**  | `/user-details/`        | Get details of the logged-in user         |
| **PUT**  | `/profile/`             | Update user profile (profile picture, name) |
| **POST** | `/logout/`              | Log out the current user                  |
| **DELETE** | `/delete-user/`       | Delete the user account                   |
| **GET**  | `/notes/`               | Get all notes for the logged-in user      |
| **POST** | `/notes/`               | Create a new note                         |
| **GET**  | `/notes/<slug>/`        | Retrieve details of a specific note       |
| **PUT**  | `/notes/<slug>/`        | Update a specific note                    |
| **DELETE** | `/notes/<slug>/`      | Delete a specific note                    |
| **GET**  | `/notes-search/?search=<query>` | Search notes by title or content  |

### 🔍 Example Usage
To access protected routes, include the `Authorization` header with your JWT token:
```
Authorization: Bearer <your-access-token>
```

## 🔧 Technologies Used
- **Django**
- **Django Rest Framework (DRF)**
- **PostgreSQL**
- **Render** for deployment
- **Cloudinary** for managing profile images
- **CORS Headers**

## 📱 Connect with Me
- Twitter: [@anuj_549](https://x.com/anuj_549)
- LinkedIn: [Anuj Chaudhary](https://www.linkedin.com/in/anujchaudhary549/)

## 🤝 Contributing
Contributions are welcome! If you'd like to contribute, please fork the repository, create a new branch, and submit a pull request.

## 📜 License
This project is licensed under the MIT License.
