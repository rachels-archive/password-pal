CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username VARCHAR(30) NOT NULL,
    password_hash CHAR(64) NOT NULL
);

CREATE TABLE credentials (
    credential_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    login_title VARCHAR(30) NOT NULL,
    login_name VARCHAR(30) NOT NULL,
    login_password CHAR(64) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE UNIQUE INDEX username ON users(username);
