const express = require('express')
const router = express.Router()
const childProcess = require('child_process')
const fs = require('fs')
const path = require('path')
const multer = require('multer')
const upload = multer({dest: 'static/uploaded_images'})

/* GET home page. */
router.post('/', upload.single('image'), function (req, res, next) {
    const fileName = req.file.filename
    console.log(fileName)
    const process = childProcess.spawn('python', ['app.py', fileName])
    process.stdout.on('data', function (data) {
        const ctPath = path.join(__dirname, "../static/cartoonized_images/" + fileName + ".jpg")
        const ctBase64 = fs.readFileSync(ctPath, 'base64')
        res.write(ctBase64)
        res.end()
    })
    process.stderr.on('error', function (err) {
        console.log("error!", err)
        res.status(500)
        res.end()
    })
})

module.exports = router;
