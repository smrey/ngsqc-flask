#username = 'sara'
#password = 'qu3rY' #way to salt and hash passwords?
username = 'testuser'
password = 'test123'
db_path = 'localhost/ngsqc'
full_db = username + ':' + password + '@' + db_path

SQLALCHEMY_TRACK_MODIFICATIONS = True #Remove in deployed version
DEBUG = True #Remove in deployed version
SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://%s' % full_db
SECRET_KEY = 'development key'

SECURITY_PASSWORD_HASH = 'sha512_crypt'
SECURITY_PASSWORD_SALT = 'salting_key'
SECURITY_TRACKABLE = True
#SECURITY_REGISTERABLE = 'True' #Removed as it didn't take account of the constraints to only allow admin users access