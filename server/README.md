# qilaihi.me server端

## 依赖版本
    python-3.5.1
    tornado-4.3

## 启动
    server.py -loggin=DEBUG -log_file_prefix=./log -port=8080 -debug=True -autoreload=True
    
## 配置
### model/__param__.py for db connection
    db = MySQLDatabase
    ip = '__ip__'
    port = 3306
    user = '__user__'
    password = '__password__'
    database = '__schema__'
    charset = '__charset__'
