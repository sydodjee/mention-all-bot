import sqlite3

class BotDatabase:
    def __init__(self, filename='database.db'):
        self.conn = sqlite3.connect(filename, check_same_thread=False)
        self._add_users_table()
        self._add_chats_table()

    def add_user(self, user_id, username):
        with self.conn:
            self.conn.execute(
                '''INSERT OR REPLACE INTO users (user_id, username) VALUES (?, ?)''',
                (user_id, username),
            )

    def get_all_users(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT user_id, username FROM users')
        return cursor.fetchall()

    def get_users_from_chat(self, chat_id):
        cursor = self.conn.cursor()
        cursor.execute(
            '''SELECT c.user_id, u.username 
               FROM chats c 
               JOIN users u on c.user_id = u.user_id 
               WHERE c.chat_id = ?''',
            (chat_id,),
        )
        return cursor.fetchall()

    def add_user_to_chat(self, chat_id, user_id):
        with self.conn:
            self.conn.execute(
                '''INSERT OR IGNORE INTO chats (chat_id, user_id) VALUES (?, ?)''',
                (chat_id, user_id),
            )

    def delete_user_from_chat(self, chat_id, user_id):
        with self.conn:
            self.conn.execute(
                '''DELETE FROM chats WHERE chat_id = ? AND user_id = ?''',
                (chat_id, user_id),
            )

    def count_users(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(user_id) FROM users')
        return cursor.fetchone()

    def count_chats(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(DISTINCT chat_id) FROM chats')
        return cursor.fetchone()

    def count_groups(self):
        cursor = self.conn.cursor()
        cursor.execute(
            '''SELECT COUNT(DISTINCT chat_id) FROM chats WHERE chat_id <> user_id'''
        )
        return cursor.fetchone()

    def _add_users_table(self):
        with self.conn:
            self.conn.execute(
                '''CREATE TABLE IF NOT EXISTS users (
                       user_id INTEGER PRIMARY KEY, 
                       username TEXT
                   )'''
            )

    def _add_chats_table(self):
        with self.conn:
            self.conn.execute(
                '''CREATE TABLE IF NOT EXISTS chats (
                       chat_id INTEGER, 
                       user_id INTEGER, 
                       PRIMARY KEY (chat_id, user_id),
                       FOREIGN KEY (user_id) REFERENCES users(user_id)
                   )'''
            )

    def close(self):
        self.conn.close()
