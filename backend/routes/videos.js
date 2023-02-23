const express = require("express");
const router = express.Router();

const multer = require("multer");
const upload = multer({ dest: "./uploads" });

router.post("/upload", upload.single("video"), (req, res) => {
    console.log("/videos/upload POST request");
    console.log(req.file);
    res.send(req.body);
});

router.post("/upload-feedback", upload.single("video"), (req, res) => {
    console.log("/videos/upload-feedback POST request");
    console.log(req.file);
    res.send(req.body);
});

module.exports = router;
