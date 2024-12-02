import sqlite3


class BotDatabase:
    def __init__(self, filename="database.db"):
        self.conn = sqlite3.connect(filename, check_same_thread=False)
        self._add_users_table()
        self._add_chats_table()

    def add_user(self, user_id, username):
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO users (user_id, username) VALUES (?, ?)",
                (user_id, username),
            )

    def get_users_from_chat(self, chat_id):
        with self.conn:
            return self.conn.execute(
                """
                SELECT c.user_id, u.username
                FROM chats c
                JOIN users u ON c.user_id = u.user_id
                WHERE c.chat_id = ?
                """,
                (chat_id,),
            ).fetchall()

    def add_user_to_chat(self, chat_id, user_id):
        with self.conn:
            self.conn.execute(
                "INSERT OR IGNORE INTO chats (chat_id, user_id) VALUES (?, ?)",
                (chat_id, user_id),
            )

    def delete_user_from_chat(self, chat_id, user_id):
        with self.conn:
            self.conn.execute(
                "DELETE FROM chats WHERE chat_id = ? AND user_id = ?",
                (chat_id, user_id),
            )

    def _add_users_table(self):
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT
                )
                """
            )

    def _add_chats_table(self):
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS chats (
                    chat_id INTEGER,
                    user_id INTEGER,
                    PRIMARY KEY (chat_id, user_id),
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
                """
            )

    def close(self):
        self.conn.close()
