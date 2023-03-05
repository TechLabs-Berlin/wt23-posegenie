const axios = require("axios");
const videoToFormData = require("./videoToFormData");

const postVideoToAServer = (endpoint, video) => {
    message = `Sending video below to ${endpoint}`;
    console.log(message, video);
    headers = {
        "Content-Type": "multipart/form-data",
    };
    return axios.post(endpoint, videoToFormData(video), headers);
};

module.exports = postVideoToAServer;
