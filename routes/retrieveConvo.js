const db = require('./db');

function loadFullResponse(userID,module) {
    const stmt = db.prepare(`SELECT full_response FROM conversations WHERE userID = ? AND module = ? LIMIT 1`);
    const row = stmt.get(userID,module);
    return row ? row.full_response : null;
}

module.exports = loadFullResponse;