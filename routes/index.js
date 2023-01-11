const express = require('express');
const router = express.Router();
const childProcess = require('child_process');
const multer = require('multer')
const storage = multer.memoryStorage()
const upload = multer({storage: storage})

/* GET home page. */
router.post('/', upload.single('dict'), function (req, res, next) {
    const fileBuffer = req.file.buffer
    const process = childProcess.spawn('!python', ['app.py', fileBuffer])
    process.stdout.on('data', function (data) {
        response.end(data)
        next()
    })
    process.on('error', function () {
        console.log("error!")
        res.status(500)
        next()
    })
})

module.exports = router;
