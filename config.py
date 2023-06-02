import redis

r = redis.Redis(host='localhost', port=6379, password='123456')


class BaseConfig:
    SECRET_KEY = "123456"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://jingcan:123456@1.14.138.236:3306/jingcan01?charset=utf8mb4"
    # Mail设置
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = '864671033@qq.com'
    MAIL_PASSWORD = 'svcmsqixucgbbbff'
    MAIL_DEFAULT_SENDER = "864671033@qq.com"

    # Cache缓存设置
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "127.0.0.1"
    CACHE_REDIS_PASSWORD = "root"
    CACHE_REDIS_PORT = 6379
    CACHE_DEFAULT_TIMEOUT = 60

    # celery配置
    # 格式：redis://:password@hostname:port/db_number
    CELERY_BROKER_URL = 'redis://:@127.0.0.1:6379/0'
    CELERY_RESULT_BACKEND = 'redis://:@127.0.0.1:6379/0'

    # 设置上传文件的路径
    UPLOADED_FILES_DEST = "static/upload/files"
    UPLOADED_IMAGE_DEST = "static/upload/images"
    EXCEL_ALLOWED_EXTENSIONS = ["xlsx"]
    IMAGE_ALLOWED_EXTENSIONS = ["jpg", 'png', 'jpeg']


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/chatgpt?charset=utf8mb4"


class ProductiongConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://jcdata:123456@127.0.0.1:3306/jcdata?charset=utf8mb4"
    # Mail设置
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = '864671033@qq.com'
    MAIL_PASSWORD = 'svcmsqixucgbbbff'
    MAIL_DEFAULT_SENDER = "864671033@qq.com"

    # Cache缓存设置
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "127.0.0.1"
    CACHE_REDIS_PASSWORD = "root"
    CACHE_REDIS_PORT = 6379
    CACHE_DEFAULT_TIMEOUT = 60

    # celery配置
    # 格式：redis://:password@hostname:port/db_number
    CELERY_BROKER_URL = 'redis://:@127.0.0.1:6379/0'
    CELERY_RESULT_BACKEND = 'redis://:@127.0.0.1:6379/0'

    # 设置上传文件的路径
    UPLOADED_FILES_DEST = "static/upload/files"
    UPLOADED_IMAGE_DEST = "static/upload/images"
    EXCEL_ALLOWED_EXTENSIONS = ["xlsx"]
    IMAGE_ALLOWED_EXTENSIONS = ["jpg", 'png', 'jpeg']
