let MongoClient = require("mongodb").MongoClient;

module.exports = {
    startMongoDBConnection: function (func) {
        MongoClient.connect("mongodb://localhost:27017/", function (err, db) {
            let database = db.db("lamp_webchat");
            database.createCollection("users", function (err, res) {
                console.log("create collection `users`");
            });
            database.createCollection("group", function (err, res) {
                console.log("create collection `group`");
            });
            database.createCollection("group_message", function (err, res) {
                console.log("create collection `group_message`");
            });
            func(database);
        });
    }
};
