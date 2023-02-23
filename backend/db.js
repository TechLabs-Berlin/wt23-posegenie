const mongoose = require("mongoose");
mongoose.set("strictQuery", false);
require("dotenv").config();

db_uri = `mongodb+srv://
${process.env.DB_USER}:${process.env.DB_PASS}
@cluster0.o2q8c1n.mongodb.net/${process.env.DB_NAME}
?retryWrites=true&w=majority`;
connectDB = () => {
    mongoose
        .connect(db_uri)
        .then(() => {
            console.log(
                `Connected to MongoDB Atlas. Database: ${process.env.DB_NAME}`
            );
        })
        .catch((err) => {
            console.log(err);
        });
};

module.exports = connectDB;
