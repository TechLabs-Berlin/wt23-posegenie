const express = require("express");
const fs = require("fs");
const path = require("path");
const router = express.Router();

const multer = require("multer");
const upload = multer();
const axios = require("axios");
const FormData = require("form-data");
const AdmZip = require("adm-zip");

router.post("/upload", upload.single("video"), (req, frontendResponse) => {
    console.log("/videos/upload POST request");
    video = req.file;
    pose = req.body.pose;
    console.log(req.body);
    console.log(video);

    // create FormData object and append the file data to it
    const formData = new FormData();
    formData.append("file", video.buffer, {
        filename: video.originalname,
        contentType: video.mimetype,
    });

    formData.append("pose", pose);

    // Send the video to flask server
    url = "http://localhost:5001/process_video";
    axios
        .post(url, formData, {
            responseType: "arraybuffer",
            headers: {
                "Content-Type": "multipart/form-data",
            },
        })
        .then((res) => {
            const zip = new AdmZip(res.data);
            const zipEntries = zip.getEntries();

            let videoUrl, imageUrl;
            zipEntries.forEach((zipEntry) => {
                if (zipEntry.entryName.endsWith(".mp4")) {
                    const publicPath = path.join(__dirname, "../public/videos");
                    if (!fs.existsSync(publicPath)) {
                        fs.mkdirSync(publicPath, { recursive: true });
                    }
                    const filename = `video_${Date.now()}.mp4`;
                    fs.writeFileSync(
                        `${publicPath}/${filename}`,
                        zipEntry.getData()
                    );
                    videoUrl = `/videos/${filename}`;
                } else if (zipEntry.entryName.endsWith(".png")) {
                    const publicPath = path.join(__dirname, "../public/images");
                    if (!fs.existsSync(publicPath)) {
                        fs.mkdirSync(publicPath, { recursive: true });
                    }
                    const filename = `image_${Date.now()}.png`;
                    fs.writeFileSync(
                        `${publicPath}/${filename}`,
                        zipEntry.getData()
                    );
                    imageUrl = `/images/${filename}`;
                }
            });

            const responseData = { videoUrl, imageUrl };
            console.log(responseData);
            frontendResponse.send(responseData);
        })
        .catch((err) => console.log(err));

    // Send the response to frontend
});

router.post("/upload-feedback", upload.single("video"), (req, res) => {
    console.log("/videos/upload-feedback POST request");
    res.send(req.body);
});

module.exports = router;
