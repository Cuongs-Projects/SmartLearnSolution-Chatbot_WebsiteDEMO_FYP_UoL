// const fs = require('fs');

const dbFile = 'conversations.db';

// Delete the file if it exists
// if (fs.existsSync(dbFile)) {
//     fs.unlinkSync(dbFile);
// }

const Database = require('better-sqlite3');
const db = new Database(dbFile);

// Create the table again
db.prepare(`
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userID TEXT,
        module TEXT,
        full_response TEXT
    )
`).run();

module.exports = db;