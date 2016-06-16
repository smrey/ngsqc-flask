#username = 'sara'
#password = 'qu3rY' #way to salt and hash passwords?
username = 'testuser'
password = 'test123'
db_path = 'localhost/ngsqc'
full_db = username + ':' + password + '@' + db_path

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://%s' % full_db
USERNAME = 'admin'
PASSWORD = 'default'
SECRET_KEY = 'development key'