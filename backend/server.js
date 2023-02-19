const express = require("express");
app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
const connectDB = require("./db");
const usersRoutes = require("./routes/users");

// Start the database connection
connectDB();

// Routes
usersRoutes(app);

// Start the server
port = process.env.PORT || 3000;
app.listen(port, () => {
    console.log(`Backend server running on port ${port}`);
});
