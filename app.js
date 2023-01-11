const express = require('express');
const path = require('path');
const bodyParser = require('body-parser')

const indexRouter = require('./routes/index');

const app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));

app.use(bodyParser.json({limit: 10*1024*1024}))
app.use(bodyParser.text({limit: 10*1024*1024}))
app.use(bodyParser.raw({limit: 10*1024*1024}))
app.use(bodyParser.urlencoded({limit: 10*1024*1024}))

app.use(express.json());
app.use(express.urlencoded({extended: false}));
app.use(express.static(path.join(__dirname, 'public')));

app.all("*", function (req, res, next) {
    // 设置允许跨域的域名,*代表允许任意域名跨域
    res.header('Access-Control-Allow-Origin', '*')
    // 允许的header类型
    res.header('Access-Control-Allow-Headers', 'Origin,X-Requested-With,Content-Type,Accept,Authorization,Cookie,token')
    // 跨域允许的请求方式
    res.header('Access-Control-Allow-Methods', 'DELETE,PUT,POST,GET,OPTIONS')

    res.header('X-Requested-With', 'XMLHttpRequest')
    if (req.method.toLowerCase() === 'options')
        res.sendStatus(200);
    else
        next();
})

app.use('/', indexRouter);

app.use((req, res, next) => {
    if (res.get('status') === '500') {
        res.json({
            'msg': 'an internal error occurred:\n' + res.locals.msg
        }).end()
    } else {
        res.json({
            'msg': res.locals.msg
        })
        res.end()
    }
})

module.exports = app;
