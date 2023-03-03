const express = require("express");
const router = express.Router();

const multer = require("multer");
const upload = multer({ dest: "./uploads" });
const axios = require("axios");

router.post("/upload", upload.single("video"), async (req, res) => {
    console.log("/videos/upload POST request");
    url = "http://localhost:6000/process_video";
    console.log(req.file);
    axios
        .post(url, req.file)
        .then((res) => {
            console.log(res);
        })
        .catch((err) => {
            console.log(err.message);
        });
    res.send(req.file);
});

router.post("/upload-feedback", upload.single("video"), (req, res) => {
    console.log("/videos/upload-feedback POST request");
    res.send(req.body);
});

module.exports = router;
