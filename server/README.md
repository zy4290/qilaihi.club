# qilaihi.me server

## TODO
* 发送微信模板消息
* 同步微信多媒体文件到阿里云
* 解析微信location事件,更新用户地址
* 设计实现微信文字IVR
* “活动”页面API
* “足迹”页面API
* “我的”页面API

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
#### 1.1 地理位置搜索
接口地址:
```
    http://qilaihi.me/api/v1/place/query
```
请求数据示例:
```
    {
        "query":"东亭新嘉源",
        "region":"武汉"
    }
```
说明:
```
    region为城市名称
```
#### 2. event
##### 2.1 分页查询活动 
接口地址:
```
    http://qilaihi.me/api/v1/event/list
```
请求数据示例:
```
    {
        "page_number":1,
        "items_per_page":8
    }
```
说明：
```
    page_number从1开始
    请求数据可为{}，则默认第1页，每页4条数据
```
##### 2.2 按番号查询活动 
接口地址:
```
    http://qilaihi.me/api/v1/event/get
```
请求数据示例:
```
    {
        "code":"大王派我来巡山"
    }
```
##### 2.3 发布活动 
接口地址：
```
    http://qilaihi.me/api/v1/event/publish
```
请求数据示例：
```
    {
        "code":"唯一的番号",
        "mediaids":["media_id1", "media_id2", ...]
        "title":"活动简介"
        "time":"YYYY-MM-DD HH:mm:ss"
        "aacost":68
        "tag":"户外"
        "expectsignups":4
        "agerange":3
        "location":"东湖风景区"
        "address":"湖北省武汉市武昌区"
        "latitude":"30.575504"
        "longitude":"114.379627"
        "organizerid":"o-7des8JLh-sCql5MZ2_oSLImxdc"
    }
```
#### 3. 微信JS SDK
##### 3.1 拉取用户信息
接口地址：
```
    http://qilaihi.me/api/v1/wxweb/user/get
```
请求数据示例：
```
    {
        "code":"callback_url_code"
        "scope":"snsapi_userinfo", // 默认为snsapi_base，仅获取openid
    }
```
##### 3.1 拉取用户信息
接口地址：
```
    http://qilaihi.me/api/v1/wxweb/user/get
```
请求数据示例：
```
    {
        "code":"callback_url_code"
        "scope":"snsapi_userinfo", // 默认为snsapi_base，仅获取openid
    }
```
##### 3.2 URL签名
接口地址：
```
    http://qilaihi.me/api/v1/wxweb/url/sign
```
请求数据示例：
```
    {
        "url":"http://qilaihi.me/event?code=上山打老虎" // 该url不需要urlencode，微信所附加的#号及后面的内容需要移除
    }
```



