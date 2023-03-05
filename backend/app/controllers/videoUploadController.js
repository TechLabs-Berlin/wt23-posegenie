const postVideoToAServer = require("../../utils/postVideoToAServer");

const handleFLaskResponse = (res) => {
    console.log("Hello");
};

const handleFlaskError = (err) => {
    console.log("Something went wrong with the request.");
};

const postVideoToFlask = (video) => {
    endpoint = "http://localhost:5001/process_video";
    postVideoToAServer(endpoint, video)
        .then(handleFLaskResponse)
        .catch(handleFlaskError);
};

module.exports = {
    post: (req, res) => {
        console.log("/videos/upload POST request");
        video = req.file;
        postVideoToFlask(video);
        res.send(video);
    },
};
