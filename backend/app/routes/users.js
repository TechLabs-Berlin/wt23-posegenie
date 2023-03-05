const usersController = require("../controllers/usersController");

module.exports = (app) => {
    app.post("/users", usersController.createUser);
    app.get("/users", usersController.getAllUsers);
    app.get("/users/:id", usersController.getUserById);
    app.put("/users/:id", usersController.updateUser);
    app.delete("/users/:id", usersController.deleteUser);
};
