const axios = require("axios");
const videoToFormData = require("../../utils/videoToFormData");

const sendVideoToFlask = (video) => {
    url = "http://localhost:5001/process_video";
    headers = {
        "Content-Type": "multipart/form-data",
    };

    axios
        .post(url, videoToFormData(video), headers)
        .then((res) => console.log("Hello"))
        .catch((err) =>
            console.log("Something went wrong with " + url + " request.")
        );
};

module.exports = {
    post: (req, res) => {
        console.log("/videos/upload POST request");
        video = req.file;
        console.log(video);
        sendVideoToFlask(video);
        res.send(video);
    },
};
