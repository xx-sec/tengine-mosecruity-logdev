# 执行顺序和工作说明


```bash 

yum -y install git curl gcc gcc-c++ unzip wget 
yum -y install epel-release 
yum -y install docker-compose 

git clone https://github.com/

## 同步时区
cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

```

### 安装 Docker 
```bash 
curl https://raw.githubusercontent.com/xx-scan/xx-scan/master/_dev/install_docker.sh | sudo /bin/bash 
```


## 引擎部署

```bash 
docker run -itd -p 3380:80 -v /spool/log/:/var/log/ --restart=always --name=tengine actanble/tengine-with-modsecurity && \
docker exec -t tengine /usr/sbin/nginx
```
- 注意这个地方不能直接一行执行，或者Dockerfile执行，目前不知道原因。 


## Modsecruity 日志Scheme导入
```bash 
docker exec -i mysql-server mysql -uroot -ptest@1q2w2e4R p3 < modsecurity-log.scheme 
```

## 日志Mongo2Mysql部署
```bash 
docker build -t actanble/logdev_pytask .
docker run -itd actanble/logdev_pytask --restart=always -v ./xsqlmb:/usr/local/xsqlmb --net=host --name=pytask 
docker exec -t pytask serv.py


docker run -itd --name=pytask --restart=always \
-v $(pwd)/xsqlmb:/usr/local/xsqlmb \
tenginemosecruitylogdev_pytask /bin/bash 
```

## 宿主机 Crontab 
```
* * * * * root /usr/bin/docker exec -t pytask serv.py 
```

### bash 脚本控制到s或者使用Tornado,Apscheduler


## Tengine 绑定自己的 conf 
```bash
docker run -itd -p 3380:80 \
-v /spool/log/:/var/log/ -v $(pwd)/tengine/vhost:/etc/nginx/vhost\
--restart=always \
--name=tengine \
actanble/tengine-with-modsecurity

```

## 部署juiceshop靶场
```bash
docker run -itd -p 3000:3000 \
--name=juice-shop  bkimminich/juice-shop

```

## 最新更新
- 编译安装的版本 actanble/modsecurity 存在docker-compose 问题
- 需要改进，目前启动方法
```bash 
docker run -itd -p 3280:80 -v /spool/log/:/var/log/ \
-v $(pwd)/tengine/ \
-v /etc/localtime:/etc/localtime:ro \
-v $(pwd)/tengine/nginx.conf:/etc/nginx.conf \
-v $(pwd)/tengine/help.conf:/etc/nginx/help.conf \
-v $(pwd)/tengine/vhosts:/etc/nginx/vhosts \
  --restart=always --name=tengine actanble/modsecurity /bin/bash;
docker exec -t tengine /usr/sbin/nginx
```
