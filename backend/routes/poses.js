const express = require("express");
const router = express.Router();
const fs = require("fs");

router.get("/", (req, res) => {
    const posesFile = fs.readFileSync("./data/poses.json");
    const posesData = JSON.parse(posesFile);
    const poses = [];
    posesData.map((pose) => {
        poses.push({
            id: pose.name,
            label: pose.name,
        });
    });
    res.send(poses);
});

module.exports = router;
