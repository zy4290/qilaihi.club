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
