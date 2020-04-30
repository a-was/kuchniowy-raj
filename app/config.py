class Config:
    SECRET_KEY = '|1XdY4<?Z^;nq"0JRi?$H=P2XlFo,d'
    DEBUG = True
    PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*?]).{8,16}$'  # Pa$$w0rd


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
