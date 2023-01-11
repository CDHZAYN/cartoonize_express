
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
    res.header('Access-Control-Allow-Origin', '*')
    res.header('Access-Control-Allow-Headers', 'Origin,X-Requested-With,Content-Type,Accept,Authorization,Cookie,token')
    res.header('Access-Control-Allow-Methods', 'DELETE,PUT,POST,GET,OPTIONS')
    res.header('X-Requested-With', 'XMLHttpRequest')
    res.header('ngrok-skip-browser-warning', true)
    if (req.method.toLowerCase() === 'options')
        res.sendStatus(200);
    else
        next();
})

app.use('/', indexRouter);

module.exports = app;
