# -*- coding:utf-8 -*-
from tornado import web, ioloop
import sys
sys.path.append('..')


class MainHandler(web.RequestHandler):
    def get(self):
        self.write('Hello Tornado')


def logdev():
    #inital_all_logs()
    from xsqlmb.api.logstash.scripts.log_f_mongo2sql import LogToSql
    LogToSql(MAX_INSERT_NUM=500).modseclog_to_sql()
    LogToSql(MAX_INSERT_NUM=500).accesslog_to_sql()


if __name__ == '__main__':
    application = web.Application([
        (r'/', MainHandler),
    ])
    application.listen(8081)
    ioloop.PeriodicCallback(logdev, 3000).start()  # start scheduler 每隔5s执行一次f5s
    ioloop.IOLoop.instance().start()
