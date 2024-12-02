import sqlite3

class BotDatabase:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self._add_users_table()
        self._add_chats_table()

    def add_user(self, user_id, username):
        with self.conn:
            self.conn.execute(
                '''
                INSERT INTO users (user_id, username) VALUES (?, ?)
                ON CONFLICT(user_id) DO UPDATE SET username = ?;
                ''',
                (user_id, username, username)
            )

    def get_all_users(self):
        with self.conn:
            return self.conn.execute('SELECT user_id, username FROM users').fetchall()

    def get_users_from_chat(self, chat_id):
        with self.conn:
            return self.conn.execute(
                '''
                SELECT c.user_id, u.username
                FROM chats c
                JOIN users u ON c.user_id = u.user_id
                WHERE c.chat_id = ?;
                ''',
                (chat_id,)
            ).fetchall()

    def add_user_to_chat(self, chat_id, user_id):
        with self.conn:
            self.conn.execute(
                '''
                INSERT INTO chats (chat_id, user_id) VALUES (?, ?)
                ON CONFLICT DO NOTHING;
                ''',
                (chat_id, user_id)
            )

    def delete_user_from_chat(self, chat_id, user_id):
        with self.conn:
            self.conn.execute(
                'DELETE FROM chats WHERE chat_id = ? AND user_id = ?',
                (chat_id, user_id)
            )

    def count_users(self):
        with self.conn:
            return self.conn.execute('SELECT COUNT(user_id) FROM users').fetchone()

    def count_chats(self):
        with self.conn:
            return self.conn.execute('SELECT COUNT(DISTINCT chat_id) FROM chats').fetchone()

    def count_groups(self):
        with self.conn:
            return self.conn.execute(
                '''
                SELECT COUNT(DISTINCT chat_id)
                FROM chats
                WHERE chat_id <> user_id;
                '''
            ).fetchone()

    def _add_users_table(self):
        with self.conn:
            self.conn.execute(
                '''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT
                );
                '''
            )

    def _add_chats_table(self):
        with self.conn:
            self.conn.execute(
                '''
                CREATE TABLE IF NOT EXISTS chats (
                    chat_id INTEGER,
                    user_id INTEGER,
                    PRIMARY KEY (chat_id, user_id),
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                );
                '''
            )

    def close(self):
        self.conn.close()
