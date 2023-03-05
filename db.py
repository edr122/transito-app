from app import app
from flask_mysqldb import MySQL


# Mysql Settings
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'eder'
app.config['MYSQL_DB'] = 'transito'

# MySQL Connection
mysql = MySQL(app)