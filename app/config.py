import os
class Configuration(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://weather:weather@database_tst/cliff_report'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
