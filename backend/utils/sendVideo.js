const axios = require("axios");
const fs = require("fs");

function sendVideoToAPI(videoFilePath, poseName, APIEndpoint) {
    const video = fs.createReadStream(videoFilePath);

    axios
        .post(APIEndpoint, {
            data: video,
            headers: {
                "Content-Type": "multipart/form-data",
            },
            params: {
                poseName: poseName,
            },
        })
        .then((response) => {
            console.log(response.data);
        })
        .catch((error) => {
            console.log(error);
        });
}

module.exports = { sendVideoToAPI };
