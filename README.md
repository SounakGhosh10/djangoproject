# App Tasks Platform

A Django-based platform that allows users to complete tasks by using apps and earn points. The platform includes both admin and user interfaces.

## Features

- **Admin Interface**: Manage apps, review tasks, and monitor user activity
- **User Interface**: View available apps, submit tasks with screenshots, and earn points
- **JWT Authentication**: Secure API endpoints with token-based authentication
- **MongoDB Integration**: Store data in a NoSQL database for flexibility
- **Responsive Design**: Modern UI that works on desktop and mobile devices

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Database**: MongoDB (via Djongo)
- **Authentication**: JWT (JSON Web Tokens)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **File Storage**: Local storage for development, cloud storage for production

## Deployment on Render

This project is configured for easy deployment on Render.com's free tier.

### Prerequisites

- A GitHub account
- A Render.com account

### Deployment Steps

1. **Fork or clone this repository to your GitHub account**

2. **Connect your GitHub repository to Render**

   - Log in to Render.com
   - Click "New" and select "Blueprint"
   - Connect your GitHub account and select this repository
   - Click "Apply Blueprint"

3. **Render will automatically**:

   - Create a web service for the Django application
   - Create a MongoDB database
   - Set up the necessary environment variables
   - Deploy your application

4. **Access your deployed application**
   - Once deployment is complete, Render will provide a URL for your application
   - The URL will be in the format: `https://app-tasks-platform.onrender.com`

### Manual Deployment

If you prefer to deploy manually:

1. **Create a new Web Service on Render**

   - Select "Web Service"
   - Connect your GitHub repository
   - Name: `app-tasks-platform` (or your preferred name)
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn config.wsgi:application`

2. **Create a MongoDB database on Render**

   - Select "Database"
   - Type: MongoDB
   - Name: `mongodb`

3. **Set environment variables**
   - `SECRET_KEY`: Generate a secure random string
   - `DEBUG`: Set to `False` for production
   - `ALLOWED_HOSTS`: Add your Render domain (e.g., `.onrender.com`)
   - `DATABASE_URL`: This will be automatically set by Render

## Local Development

1. **Clone the repository**

   ```
   git clone https://github.com/yourusername/app-tasks-platform.git
   cd app-tasks-platform
   ```

2. **Create a virtual environment**

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```
   pip install -r requirements.txt
   ```

4. **Set up MongoDB**

   - Install MongoDB locally or use MongoDB Atlas
   - Update the `DATABASES` setting in `config/settings.py` if needed

5. **Run migrations**

   ```
   python manage.py migrate
   ```

6. **Create a superuser**

   ```
   python manage.py createsuperuser
   ```

7. **Run the development server**

   ```
   python manage.py runserver
   ```

8. **Access the application**
   - Admin interface: http://127.0.0.1:8000/custom-admin/login/
   - User interface: http://127.0.0.1:8000/user/login/

## License

This project is licensed under the MIT License - see the LICENSE file for details.
