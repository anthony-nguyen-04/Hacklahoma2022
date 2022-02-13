const fs = require('fs');
const path = require('path');
const userController = {};

userController.SCOPES = [
    "user",
    "validator",
    "admin"
]

userController.getUsers = function () {
    const userText = fs.readFileSync(path.join(__dirname + '/user-store.json'));
    const users = JSON.parse(userText);
    return users;
}

userController.getUser = function (username) {
    const users = userController.getUsers();
    return users[username];
}

userController.setUser = function (user) {
    const users = userController.getUsers();
    users[user.username] = user;
    userController.saveUsers(users);
}

userController.saveUsers = function (userList) {
    const userText = JSON.stringify(userList);
    fs.writeFileSync(path.join(__dirname + '/user-store.json'), userText);
}

userController.userExists = function (username) {
    const users = userController.getUsers();
    return 'username' in users;
}

userController.addUser = function (username) {
    userController.setUser({ username: username })
}

module.exports = userController;
