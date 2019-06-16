# coding:utf-8
import sys
import re
from xsqlmb.api.logstash.utils.dt_tool import get_pydt_based_logdt
from xsqlmb.api.logstash.cfgs.configs import WAF_ACCESS_LOG_SQL_TABLE, \
    WAF_ALERT_LOG_SQL_TABLE, WAF_ALERT_LOG_DETAILED_SQL_TABLE
#from utils.django_module import django_setup
try:
    from xsqlmb.src.cfgs.logConfig import logging
except:
    import logging

from uuid import uuid4
from xsqlmb.api.logstash.scripts.extract_log_f_mongo import ExtractLogFromMongo
from xsqlmb.src.dao.exutil import MutiTypesInsets2SqlClass
#from xsqlmb.src.ltool.sqlconn import from_sql_get_data, sql_action
from xsqlmb.api.logstash.utils.get_table_columns import get_waf_alert_log_columns, get_waf_access_log_columns
from ..cfgs.configs import WAF_ACCESS_LOG_SQL_TABLE, WAF_ALERT_LOG_SQL_TABLE

_waf_columns = get_waf_alert_log_columns()

class LogToSql():

    def __init__(self, MAX_INSERT_NUM=500):
        self.MAX_INSERT_NUM=MAX_INSERT_NUM

    def init_sql_logdb(self):
        pass

    def get_latest_accsslog(self):
        datas, line = ExtractLogFromMongo(table_name=WAF_ACCESS_LOG_SQL_TABLE).get_access_logs()
        return datas

    def get_latest_modseclog(self):
        return ExtractLogFromMongo(table_name=WAF_ALERT_LOG_SQL_TABLE).modseclog_to_detaild()

    def many_insert2_accesslog(self, nad_datas):
        from django.core.paginator import Paginator
        p = Paginator(nad_datas, self.MAX_INSERT_NUM) # 分页列别
        page_count = p.num_pages  # 总页数
        seccess_insert_num = 0

        # from xsqlmb.api.logstash.utils.get_table_columns import get_waf_access_log_columns
        cols = get_waf_access_log_columns()
        _columns = "`" + "`, `".join(cols) + "`"
        _keys = cols

        for x in [x+1 for x in range(page_count)]:
            nad_list = list(p.page(x).object_list)
            from xsqlmb.src.dao.exutil import MutiTypesInsets2SqlClass
            MutiTypesInsets2SqlClass(table_name = WAF_ACCESS_LOG_SQL_TABLE).arrays2sql2(
            nad_list, columns_order=_columns, keys_list=_keys)
            seccess_insert_num += len(nad_list)

        return seccess_insert_num

    def accesslog_to_sql(self, local=False):
        nad_datas = []
        _accesslog_datas = self.get_latest_accsslog()
        for x in _accesslog_datas:
            obj = x.copy()
            try:
                obj["time_local"] = get_pydt_based_logdt(re.match("(.*?)\s(.*)", obj["time_local"]).group(1))
                obj["timestamp"] = obj["time_local"]

                if "request_url" not in obj.keys():
                    obj["request_url"] = obj["url"]

                if "request_id" not in obj.keys():
                    obj["request_id"] = uuid4()

                obj["upstream_response_time"] = "0.01" if obj["upstream_response_time"] == "-" else "0.0"
                obj["request_time"] = "0.01" if obj["upstream_response_time"] == "-" else "0.0"
            except:
                logging.error("Error:存在AccessLog日志不一样的正则 " + obj["time_local"])

                continue
            nad_datas.append(obj)
        seccess_insert_num = self.many_insert2_accesslog(nad_datas)

        logging.info("插入【" + str(seccess_insert_num)  +"】条新数据到访问日志SQL数据库成功")

    def modseclog_to_sql(self):
        # from datetime import datetime
        # default_time = datetime(1995, 8, 14)
        nad_datas = self.get_latest_modseclog()

        from django.core.paginator import Paginator
        p = Paginator(nad_datas, self.MAX_INSERT_NUM)  # 分页列别
        page_count = p.num_pages  # 总页数
        seccess_insert_num = 0

        from xsqlmb.api.logstash.utils.get_table_columns import get_waf_alert_log_columns
        cols = get_waf_alert_log_columns()

        _columns = "`" + "`, `".join(cols) + "`"
        _keys = cols

        for x in [x + 1 for x in range(page_count)]:
            nad_list = list(p.page(x).object_list)
            try:
                _insert_num = MutiTypesInsets2SqlClass(table_name=WAF_ALERT_LOG_SQL_TABLE).arrays2sql2(
                    nad_list, columns_order=_columns, keys_list=_keys)
                seccess_insert_num += _insert_num

            finally:
                import json

                # _detailed_list = [ [x["audit_logid"], json.dumps(x)] for x in nad_list ]
                # MutiTypesInsets2SqlClass(table_name=WAF_ALERT_LOG_DETAILED_SQL_TABLE).arrays2sql(
                #     _detailed_list, columns_order="`audit_logid`,`detaild`"
                # )
                _detailed_list = [dict(audit_logid=x["audit_logid"], detaild=json.dumps(x) ) for x in nad_list]

                from xsqlmb.src.ltool.mongo import MongoConn
                from xsqlmb.api.logstash.cfgs.configs import WAF_ALERT_LOG_DETAILED_SQL_TABLE
                MongoConn().insert_data(WAF_ALERT_LOG_DETAILED_SQL_TABLE, _detailed_list)


        logging.info("插入【" + str(seccess_insert_num) + "】条新数据到告警日志SQL数据库成功")





