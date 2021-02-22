let server = require("ws");
let utils = require("./utils");
let router = require("./router");
let settings = require("./settings");


utils.startMongoDBConnection((db) => {
    startWebSocketServer(db);
});

function startWebSocketServer(db) {
    let port = 8008;

    let socket = new server.Server({
        port: port
    });

    console.log(`Started server on port: ${port}`);

    socket.on('connection', function (ws) {

        let address = ws._socket.remoteAddress;
        let port = ws._socket.remotePort;

        settings.serverSettings.connected_users += 1;
        settings.serverSettings.connections[`${address}:${port}`] = ws;
        console.log("New connection: " + `${address}:${port}`);
        console.log(settings.serverSettings.connected_users);

        ws.on('message', function (message) {
            // console.log('INFO: Received new message: ' + message);
            // try to convert message to object
            try {
                let m = JSON.parse(message);
                // if ok, then process message
                let response_data = router.processMessage(m, ws, db);
                if (response_data !== -1) {
                    let response = JSON.stringify(response_data);
                    ws.send(response);
                    // console.log(`INFO: Response: '${response}'`)
                }

            } catch (e) {
                console.log("ERROR: " + e.message);
                ws.send(JSON.stringify({"code": 500, "message": e.message}));
            }

        });

        ws.on('close', function () {
            console.log('Connection closed: ' + settings.serverSettings.connected_users);
            delete settings.serverSettings.connections[`${address}:${port}`];
            db.collection("user").updateOne({'online_id': settings.serverSettings.connected_users}, {
                $set: {
                    'online': false,
                }
            });
        });

    });
}