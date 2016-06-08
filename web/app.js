/**
 * Created by zhangyan on 16-6-8.
 */

var express = require('express');
var app = express();
var bodyParser = require('body-parser');
app.use(bodyParser.json());

var ng = require('nodegrass');
var REQ_HEADERS = {
    'content-type': 'application/json'
};

// 这是静态页面的例子，后面的类似添加
app.get('/', function (req, res) {
    res.sendfile("app/index.html")
});

app.get('/event', function (req, res) {
    res.sendfile("app/event.html")
});

// 这是动态请求的例子，后面类似添加
app.post('/api/v1/place/query', function (req, res) {
    ng.post("http://qilaihi.me/api/v1/place/query",
        function (result, status, header) {
            console.log(typeof(result));
            console.log(result);
            res.send(result)
        },
        REQ_HEADERS,
        JSON.stringify(req.body),
        'utf8').on('error', function (e) {
        console.log("error:" + e.message);
    });
});

app.listen(3000);
