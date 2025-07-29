// const fs = require('fs');

const dbFile = 'conversations.db';

const Database = require('better-sqlite3');
const db = new Database(dbFile);

// Create the table again
// the table is created whenever the retrieveConvo or saveConvo is called
// as they calls db.prepare
db.prepare(`
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userID TEXT,
        module TEXT,
        full_response TEXT
    )
`).run();

module.exports = db;