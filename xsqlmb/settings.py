
LoggerSettings = dict(
  host="192.168.123.55",
  port=24224
)

# MongoConfig = dict(host='192.168.2.175', port=27017, db_name='fluent', username="root", password="test@1q2w2e4R")
MongoConfig = dict(host='192.168.123.41', port=27017, db_name='fluentd_log', username=None, password=None)

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'p3',
            'USER': 'root',
            'PASSWORD': 'test@1q2w2e4R',
            'HOST': "192.168.123.101",
            'PORT': 3306,
        }
    }
