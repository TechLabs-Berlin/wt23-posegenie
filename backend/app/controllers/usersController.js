const User = require("../models/user");

exports.createUser = async (req, res) => {
    const { username, password } = req.body;

    try {
        const user = await User.create({ username, password });
        res.json(user);
    } catch (error) {
        res.status(500).json(error.message);
    }
};

exports.getAllUsers = async (req, res) => {
    try {
        const users = await User.find({}, "username");
        res.json(users);
    } catch (error) {
        console.error(error);
        res.status(500).json(error.message);
    }
};

exports.getUserById = async (req, res) => {
    const { id } = req.params;

    try {
        const user = await User.findById(id);
        if (!user) {
            return res.status(404).json({ message: "User not found" });
        }
        res.json(user);
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: "Error retrieving user" });
    }
};

exports.updateUser = async (req, res) => {
    const { id } = req.params;
    const { username, password } = req.body;

    try {
        const user = await User.findByIdAndUpdate(
            id,
            { username, password },
            { new: true }
        );
        if (!user) {
            return res.status(404).json({ message: "User not found" });
        }
        res.json(user);
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: "Error updating user" });
    }
};

exports.deleteUser = async (req, res) => {
    const { id } = req.params;

    try {
        const user = await User.findByIdAndDelete(id);
        if (!user) {
            return res.status(404).json({ message: "User not found" });
        }
        res.json(user);
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: "Error deleting user" });
    }
};
