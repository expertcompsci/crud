# Configuration see app.config.from_object('config') in __init__.py
#   Database
import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'ai_papers.db')
#   Security
WTF_CSRF_ENABLED = True
SECRET_KEY = 'd675d572-58e9-4667-b988-4ab1de50a24c'
