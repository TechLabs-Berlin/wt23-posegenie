const express = require("express");
app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const usersRoutes = require("./routes/users");
const videosRoutes = require("./routes/videos");

// Routes
usersRoutes(app);
app.use("/videos", videosRoutes);

module.exports = app;
