let controllers = require("./controller");
let index = require("./index");
let settings = require("./settings");


module.exports = {
    processMessage: function (message, ws, db) {
        // router
        try {
            if (message.action === 'presence') {
                return controllers.presence(message, ws, db, settings.serverSettings.connected_users);
            } else if (message.action === 'create_group') {
                return controllers.create_group(message, ws, db)
            } else if (message.action === 'group_message') {
                return controllers.group_message(message, ws, db, settings.serverSettings.connections);
            } else if (message.action === 'add_user_to_group') {
                return controllers.add_user_to_group(message, ws, db);
            } else if (message.action === 'get_group_messages') {
                return controllers.get_group_messages(message, ws, db);
            }
            else {
                // exception
                return {"code": 500, "message": "Invalid request. Action was not found."}
            }
        } catch (e) {
            return {"code": 500, "message": e.message}
        }

    }
};
