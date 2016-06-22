/**
 * Created by zhangyan on 16-6-8.
 */

var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var path = require('path');
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname,'/public')));

var ng = require('nodegrass');
var REQ_HEADERS = {
    'content-type': 'application/json'
};

// 这是静态页面的例子，后面的类似添加
app.get('/', function (req, res) {
    res.sendfile("app/index.html")
});
app.get('/placeList', function (req, res) {
    res.sendfile("app/placeList.html")
});
app.get('/releaseSuccess', function (req, res) {
    res.sendfile("app/releaseSuccess.html")
});
app.get('/release', function (req, res) {
    res.sendfile("app/release.html")
});
app.get('/actDetail', function (req, res) {
    res.sendfile("app/actDetail.html")
});
app.get('/signUpSuccess', function (req, res) {
    res.sendfile("app/signUpSuccess.html")
});
app.get('/searchCode', function (req, res) {
    res.sendfile("app/searchCode.html")
});
app.get('/actPublish', function (req, res) {
    res.sendfile("app/actPublish.html")
});
/*test*/
app.get('/test_downloadpic', function (req, res) {
    res.sendfile("app/test_downloadpic.html")
});

// 这是动态请求的例子，后面类似添加
//地址查询
app.post('/api/v1/place/query', function (req, res) {
    /*if(!res.success){
        console.log('失败');
    }
    else{console.log('成功')}*/
    ng.post("http://qilaihi.me/api/v1/place/query",
        function (result, status, header) {
            //console.log(typeof(result));
            //console.log(result);
            res.send(result)
        },
        REQ_HEADERS,
        JSON.stringify(req.body),
        'utf8').on('error', function (e) {
        console.log("error:" + e.message);
    });
});
//番号查询
app.post('/api/v1/event/get', function (req, res) {

    ng.post("http://qilaihi.me/api/v1/event/get",
        function (result, status, header) {
            //console.log(typeof(result));
            //console.log(result);
            res.send(result)
        },
        REQ_HEADERS,
        JSON.stringify(req.body),
        'utf8').on('error', function (e) {
        console.log("error:" + e.message);
    });
});
//发布活动
app.post('/api/v1/event/publish', function (req, res) {
    ng.post("http://qilaihi.me/api/v1/event/publish",
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


app.listen(3001);
