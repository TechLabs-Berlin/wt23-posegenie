const express = require("express");
const router = express.Router();
const videoUploadController = require("../controllers/videoUploadController");

const multer = require("multer");
const upload = multer();

router
    .route("/upload")
    .post(upload.single("video"), videoUploadController.post);

module.exports = router;
