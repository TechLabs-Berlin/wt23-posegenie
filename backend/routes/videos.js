const express = require("express");
const router = express.Router();

const multer = require("multer");
const upload = multer();
const axios = require("axios");
const FormData = require("form-data");

router.post("/upload", upload.single("video"), (req, res) => {
    console.log("/videos/upload POST request");
    video = req.file;
    console.log(video);

    // create FormData object and append the file data to it
    const formData = new FormData();
    formData.append("file", video.buffer, {
        filename: video.originalname,
        contentType: video.mimetype,
    });

    // Send the video to flask server
    url = "http://localhost:5001/process_video";
    axios
        .post(url, formData, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        })
        .then((res) => {
            console.log(res.status);
        })
        .catch((err) => console.log(err));
    res.send(video.buffer);

    // Send the response to frontend
});

router.post("/upload-feedback", upload.single("video"), (req, res) => {
    console.log("/videos/upload-feedback POST request");
    res.send(req.body);
});

module.exports = router;
