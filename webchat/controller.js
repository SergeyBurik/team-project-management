let db_tools = require("./db_tools");

module.exports = {
    presence: function (message, ws, db, connected_users) {
        // try to find such user
        let address = ws._socket.remoteAddress;
        let port = ws._socket.remotePort;


        db.collection("users").findOne({
            'username': message.username,
            "password": message.password

        }, function (err, user) {
            if (err) throw err.message;
            if (user != null && user.username) {
                // make it online and set socket
                db.collection("users").updateOne({"username": message.username}, {
                    $set: {
                        'online': true,
                        'online_id': `${address}:${port}`
                    }
                }, function (err, res) {
                    if (err) return {"code": 500, "message": err.message};
                });
            } else {
                // create user
                let f_name = message.name.first_name;
                let l_name = message.name.last_name;

                db.collection("users").insertOne({
                    username: message.username,
                    password: message.password,
                    first_name: f_name,
                    last_name: l_name,
                    online: true,
                    online_id: `${address}:${port}`,
                }, function (err, res) {
                    if (err) throw err.message;
                })
            }
        });

        return {'code': 200}
    },

     add_user_to_group: function (message, ws, db) {
        // if user is not in group
        db_tools.get(db, "group", {"id": message.group_id}, (err, res) => {
            if (res.users.includes(message.from_user)) {
                throw "User is already in group.";
            }
        });

        // update group
        db.collection("group").updateOne({"id": message.group_id}, {
            $push: {
                "users": message.from_user
            }
        }, function (err, res) {
            if (err) throw err.message;
        });
        return {"code": 200};
    },

    create_group: function (message, ws, db) {
        let users = [];

        // if such users exist
        for (let username of message.users) {
            db.collection("users").findOne({"username": username}, function (err, res) {
                if (res != null && res.username) {
                    users.push(res.username);
                }
            });
        }

        db.collection('group').insertOne({'id': message.group_id, 'users': users});
        return {"code": 200}
    },
    group_message: function (message, ws, db, connections) {
        // send message to group
        // console.log(Object.keys(connections));
        // find group
        db.collection("group").findOne({'id': message.group_id}, function (err, group) {
            // get user
            db.collection("users").findOne({
                    'username': message.username,
                }, function (err, user) {
                if (err) throw err.message;

                // if group exists
                if (group != null && group.id) {
                    // if such user in group exists
                    if (group.users.includes(message.username)) {
                        // send to every user in group
                        sendToGroup(group, message.username, ws)
                    } else {
                        // if user is not in this group
                        throw "User is not a group member,"
                    }
                    // save sent message
                    db.collection("group_message").insertOne({
                        "time": Date.now() / 1000,
                        'from_user': message.username,
                        'to_group': group.group_id,
                        'message_text': message.message_text
                    }, function (err, res) {
                        if (err) throw err.message;
                    });
                } else {
                    throw "Group does not exists."
                }
            });

        });

        function sendToGroup(group, sender, ws) {
            for (let user of group.users) {
                //get user

                db.collection("users").findOne({"username": user}, function (err, res) {
                    // get user socket
                    if (res != null && res.online && res.username !== sender) {
                        try {
                            connections[res.online_id].send(JSON.stringify({
                                'action': 'group_message',
                                'from_user': message.username,
                                'to_group': group.id,
                                'message_text': message.message_text
                            }));
                        } catch (e) {
                            // user offline
                        }
                    }
                });
            }
        }

        return {"code": 200, "action": "group_message"}
    },
    get_group_messages: function (message, ws, db) {
        db.collection("group_messages").find({"group_id": message.group_id}).toArray((err, result) => {
            if (err) throw err;
            ws.send(JSON.stringify({"code": 200, "messages": result}));
        });
        return -1;
    }
};
