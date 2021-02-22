
module.exports = {

    get: function (db, col, query, cb) {
        db.collection(col).findOne(query, function (err, res) {
            cb(err, res);
        });
    }

}