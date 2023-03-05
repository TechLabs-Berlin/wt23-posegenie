const FormData = require("form-data");

const videoToFormData = (video) => {
    const formData = new FormData();
    formData.append("file", video.buffer, {
        filename: video.originalname,
        contentType: video.mimetype,
    });
    return formData;
};

module.exports = videoToFormData;
