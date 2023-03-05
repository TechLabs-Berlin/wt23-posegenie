const app = require("./app");
const connectDB = require("./db");
connectDB();

// Start the server
port = process.env.PORT || 5000;
app.listen(port, () => {
    console.log(`Backend server running on port ${port}`);
});
