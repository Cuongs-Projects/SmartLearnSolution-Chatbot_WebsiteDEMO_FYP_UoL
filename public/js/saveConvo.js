const db = require('./db');

function saveFullResponse(userID,module, full_response) {
    const stmt = db.prepare(`
        UPDATE conversations
        SET full_response = ?
        WHERE userID = ? AND module = ?
    `);
    const result = stmt.run(full_response, userID, module);

    // If no rows were updated (userID doesn't exist), insert instead
    if (result.changes === 0) {
        const insertStmt = db.prepare(`
            INSERT INTO conversations (userID, module,full_response)
            VALUES (?, ?, ?)
        `);
        insertStmt.run(userID, module, full_response);
    }
}

module.exports = saveFullResponse;