# qilaihi.me server

## 依赖
    Python 3.5.1+
    
    tornado (4.3)
    peewee (2.8.1)
    PyMySQL (0.7.4)

## 启动
    chmod +x $REPO_PATH/server/server.py
    server.py -logging=DEBUG -log_file_prefix=./log -port=8080 \
    -debug=True -autoreload=True
    
## 配置
### # model/__param__.py for db connection
    db = PooledMySQLDatabase
    max_connection = 100
    stale_timeout = None
    ip = '__ip__'
    port = 3306
    user = '__user__'
    password = '__password__'
    database = '__schema__'
    charset = '__charset__'
    
## 接口
### 0. 前提
服务请求类型**POST**，数据格式**JSON**，编码**UTF-8**
返回格式示例：
```
{
    "status":1,
    "msg":"ok",
    "result":{
        ...
    }
}
```
注：status=1则服务正常，status=-1则服务异常
### 1. 地理位置服务接口
#### 1.1 place 检索地理位置信息
```
接口地址:
    http://qilaihi.me/api/v1/place/query
请求数据示例:
    {
        "query":"东亭新嘉源",
        "region":"武汉"
    }
说明:
    region为城市名称
```
#### 2. event
##### 2.1 list 
分页查询活动
```
接口地址:
    http://qilaihi.me/api/v1/event/list
请求数据示例:
    {
        "page_number":1,
        "items_per_page":8
    }
说明：
    page_number从1开始
    请求数据可为{}，则默认第1页，每页4条数据
```
#### 2.2 get 
按番号查询活动
```
接口地址:
    http://qilaihi.me/api/v1/event/get
请求数据示例:
    {
        "code":"大王派我来巡山"
    }
```
#### 2.3 publish 
发布活动
```
接口地址：
    http://qilaihi.me/api/v1/event/publish
数据结构：
    Table: event
    Columns:
    id	int(11) AI PK
    code	varchar(10)
    status	int(1)
    imgurls	text
    title	varchar(200)
    viewcount	int(11)
    focuscount	int(11)
    time	datetime
    aacost	int(11)
    tag	varchar(5)
    singupcount	int(11)
    expectsignups	int(11)
    agerange	int(1)
    telephone	varchar(100)
    location	varchar(500)
    address	varchar(2000)
    latitude	varchar(100)
    longitude	varchar(100)
    likecount	int(11)
    dislikecount	int(11)
    createtime	datetime
    updatetime	datetime
    organizerid	int(11)
```


