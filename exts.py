from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_caching import Cache

# 调用Mail
mail = Mail()

# 调用SQLAlchemy
db = SQLAlchemy()

# 调用Cache
cache = Cache()
