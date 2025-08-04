from pathlib import Path
import os
import dj_database_url  # ✅ Ensure installed

BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ Secure handling
SECRET_KEY = os.getenv('SECRET_KEY', 'unsafe-default')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['.onrender.com', 'localhost']

# ✅ Security for session and CSRF cookies
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# ✅ Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

# ✅ Middleware with WhiteNoise
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ✅ Root URL Configuration
ROOT_URLCONF = 'water_delivery.urls'

# ✅ Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ✅ WSGI application
WSGI_APPLICATION = 'water_delivery.wsgi.application'

# ✅ Database (fallback to SQLite, use PostgreSQL via env DATABASE_URL)
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}

# ✅ Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ✅ Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ✅ Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'azolaqakaqu@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'  # Replace with your actual app password

# ✅ Auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ✅ Custom user model
AUTH_USER_MODEL = 'core.User'

# ✅ Custom authentication backend
AUTHENTICATION_BACKENDS = [
    'core.backends.IDNumberAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]
