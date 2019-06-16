# 执行顺序和工作说明

```bash 

yum -y install git curl gcc gcc-c++ unzip wget 
yum -y install epel-release 
yum -y install docker-compose 

git clone https://github.com/
```

### 安装 Docker 
```bash 
curl https://raw.githubusercontent.com/xx-scan/xx-scan/master/_dev/install_docker.sh | sudo /bin/bash 
```


## 引擎部署

```bash 
docker run -itd -p 3380:80 -v /spool/log/:/var/log/ --name=tengine actanble/tengine-with-modsecurity && \
docker exec -t tengine /usr/sbin/nginx
```
- 注意这个地方不能直接一行执行，或者Dockerfile执行，目前不知道原因。 


## Modsecruity 日志Scheme导入
```bash 
docker exec -t mysql-server mysql -uroot -ptest@1q2w2e4R p3 < modsecurity-log.scheme 
```

## 日志Mongo2Mysql部署
```bash 
docker build -t actanble/logdev_pytask .
docker run -itd actanble/logdev_pytask -v ./xsqlmb:/usr/local/xsqlmb --net=host --name=pytask 
docker exec -t pytask serv.py
```

## 宿主机 Crontab 
```
* * * * * root docker exec -t pytask serv.py 
```

### bash 脚本控制到s或者使用Tornado,Apscheduler
