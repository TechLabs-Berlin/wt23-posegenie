const express = require("express");
app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
const connectDB = require("./db");
const usersRoutes = require("./routes/users");
const videosRoutes = require("./routes/videos");
const posesRoutes = require("./routes/poses");

// Start the database connection
connectDB();

// Routes
usersRoutes(app);
app.use("/videos", videosRoutes);
app.use("/poses", posesRoutes);

// Start the server
port = process.env.PORT || 5000;
app.listen(port, () => {
    console.log(`Backend server running on port ${port}`);
});
