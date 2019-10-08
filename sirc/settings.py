import os

import django_heroku


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = os.environ.get('DEBUG', False)

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS")

INSTALLED_APPS = [
    # "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "sirc.core",
    "sirc.apps.SircAdminConfig",
    "admin_reorder",
    "tinymce",
    "compressor",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "admin_reorder.middleware.ModelAdminReorder",
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

# admin_reorder SETTINGS
ADMIN_REORDER = (
    {
        "app": "core",
        "label": "Usuários",
        "models": ({"model": "core.Usuario", "label": "Ver usuários"},),
    },
    {
        "app": "core",
        "label": "SIRC",
        "models": (
            {"model": "core.Anais", "label": "Ver ediçoes anteriores"},
            {"model": "core.Sirc", "label": "Ver edições"},
            {"model": "core.Palestras", "label": "Ver palestras"},
            {"model": "core.Palestrantes", "label": "Ver palestrantes"},
            {"model": "core.Local", "label": "Ver locais"},
        ),
    },
    {
        "app": "core",
        "label": "Contatos",
        "models": ({"model": "core.Contato", "label": "Ver contatos"},),
    },
    {
        "app": "core",
        "label": "Paginas",
        "models": ({"model": "core.Paginas", "label": "Ver páginas"},),
    },
    {
        "app": "core",
        "label": "Notícias",
        "models": ({"model": "core.Noticias", "label": "Ver notícias"},),
    },
    {
        "app": "core",
        "label": "Patrocinadores",
        "models": ({"model": "core.Patrocinador", "label": "Ver patrocinadores"},),
    },
    {
        "app": "core",
        "label": "Organizadores",
        "models": ({"model": "core.Organizadores", "label": "Ver organizadores"},),
    },
    {
        "app": "core",
        "label": "Formatos de Submissão",
        "models": ({"model": "core.Formatos", "label": "Ver formatos"},),
    },
    {
        "app": "core",
        "label": "Datas Importantes",
        "models": ({"model": "core.Datas", "label": "Ver datas"},),
    },
)

ROOT_URLCONF = "sirc.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "sirc.wsgi.application"

""" DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('dbname'),
        'USER': os.environ.get('user'),
        'PASSWORD': os.environ.get('password'),
        'HOST': os.environ.get('host'),
        'PORT': os.environ.get('port'),
    }
} """

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "database.db"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTH_USER_MODEL = "core.Usuario"

AUTHENTICATION_BACKENDS = (("django.contrib.auth.backends.ModelBackend"),)

LANGUAGE_CODE = "pt-BR"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

django_heroku.settings(locals())