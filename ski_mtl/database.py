import os
from flaskext.sqlalchemy import SQLAlchemy
from ski_mtl import app

if 'DATABASE_URL' in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
else:
    import getpass
    user = "philippemongeau"
    pswd = getpass.getpass("Password: ")
    app.config['SQLALCHEMY_DATABASE_URI'] = \
            'postgresql+psycopg2://{}:{}@/ski_mtl_test'.format(user, pswd)


db = SQLAlchemy(app)
