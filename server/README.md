# qilaihi.me server

## Todo List
* 微信消息和事件
  * 用户关注，更新用户信息
  * 上报地理位置，更新用户信息
  * 根据带参数二维码，推送活动单图文
* 微信文字IVR
  * \#番号-按番号模糊查询，推送活动图文
  * ?-根据用户偏好随机推送本地区活动图文
  * $/￥-获取红包口令
* “活动”页面API
  * 关注活动
  * 参加活动
  * 评论
  * 评分（人）
  * 评分（活动）
* “足迹”页面API
* “我的”页面API

## 依赖
    Python 3.5.1+
    
    tornado (4.3)
    peewee (2.8.1)
    PyMySQL (0.7.4)

## 启动
    python3.5 server.py -logging=DEBUG -log_file_prefix=./8080.log -port=8080 \
    -debug=True -autoreload=True
    python3.5 refresh_access_token.py -log_file_prefix=./token.log
    python3.5 sync_media_file.py -log_file_prefix=./media.log
    
## 配置
### 1 数据库配置
config/db.py
```
db = RetryPooledMySQLDB
max_connection = 20
stale_timeout = 60
ip = 'qilaihi.me'
port = 3306
user = 'root'
password = '98027531z'
database = 'qilaihi'
charset = 'utf8'
```
### 2 文件同步配置
config/sync.py
```
start_at = 0
stop_at = 24
store_at = None
default_name = 'media'

ftp_server = 'qilaihi.me'
ftp_port = 2048
ftp_user = 'Bmu2UkXJfEhgKnEQ/qilaihi-upload'
ftp_password = 'TVyUpvMoaythoGaw4t02I4kohCxZ9e'

url_prefix = 'http://u.qilaihi.me/'
```
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



