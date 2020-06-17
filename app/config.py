from datetime import timedelta


class Config:
    DEBUG = True
    SECRET_KEY = '|1XdY4<?Z^;nq"0JRi?$H=P2XlFo,d'

    DB_FILE = 'database.sqlite3'
    USERNAME_REGEX = r'^[a-zA-Z0-9]{4,12}$'
    PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*?]).{8,16}$'  # Pa$$w0rd
    RECIPE_NAME_REGEX = r'^[a-zA-Z0-9 -\/!():\'".,?]{5,75}$'

    PERMANENT_SESSION_LIFETIME = timedelta(hours=12)

    DAILY_RECIPE_FILE = 'app/static/cache/daily_recipe.cache'


LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)-5s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'app': {
            'level': 'DEBUG',
            'handlers': ['console', ]
        }
    },
}
