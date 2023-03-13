const express = require("express");
const fs = require("fs");
const router = express.Router();

const multer = require("multer");

const storage = multer.diskStorage({
  destination: "./uploads",
  filename: function (req, file, cb) {
    cb(null, Date.now() + "-" + file.originalname);
  },
});

const upload = multer({ storage: storage });

router.post("/upload", upload.single("video"), (req, res) => {
  const content = {
    filePath: req.file.path,
  };

  res.end(JSON.stringify(content));
});

router.post("/upload-feedback", upload.single("video"), (req, res) => {
  console.log("/videos/upload-feedback POST request");
  console.log(req.file);
  res.send(req.file.path);
});

router.get("/uploads/:filename", (req, res) => {
  const filePath = `./uploads/${req.params.filename}`;
  if (!filePath) {
    return res.status(404).send("File not found");
  }

  const stat = fs.statSync(filePath);
  const fileSize = stat.size;
  const head = {
    "Content-Length": fileSize,
    "Content-Type": "video/mp4",
  };
  res.writeHead(200, head);
  fs.createReadStream(filePath).pipe(res);
});

module.exports = router;
