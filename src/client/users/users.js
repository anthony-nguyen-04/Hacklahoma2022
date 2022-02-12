const fs = require('fs');
const userController = {};

userController.SCOPES = [
    "user",
    "validator",
    "admin"
]

userController.getUsers = function () {
    const userText = fs.readFileSync('./user-store.json');
    const users = JSON.parse(userText);
    return users;
}

userController.getUser = function (username) {
    const users = userController.getUsers();
    return users[username];
}

userController.setUser = function (user) {
    const users = userController.getUsers();
    users[username] = user;
    userController.saveUsers(users);
}

userController.saveUsers = function (userList) {
    const userText = JSON.stringify(userList);
    fs.writeFileSync('./user-store.json', userText);
}
