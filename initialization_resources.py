import sqlite3

class InitialTables:
    """
    A class to handle the creation of initial tables for a database.
    """

    def __init__(self):
        self.user_table_query = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            bio_by_user TEXT DEFAULT NULL
        )'''

        self.twits_table_query = '''
        CREATE TABLE IF NOT EXISTS twits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )'''

        self.follows_table_query = '''
        CREATE TABLE IF NOT EXISTS follows (
            follower_id INTEGER NOT NULL,
            being_followed_id INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (follower_id, being_followed_id),
            FOREIGN KEY (follower_id) REFERENCES users(id),
            FOREIGN KEY (being_followed_id) REFERENCES users(id)
        )'''

        self.likes_table_query = '''
        CREATE TABLE IF NOT EXISTS likes (
            user_id INTEGER NOT NULL,
            twit_id INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, twit_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (twit_id) REFERENCES twits(id)
        )'''

    def create_tables(self, db_connection):
        """
        Create tables in the database using the provided connection.
        """
        queries = [self.user_table_query, self.twits_table_query, self.follows_table_query, self.likes_table_query]
        
        try:
            cursor = db_connection.cursor()
            for query in queries:
                cursor.execute(query)
            db_connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

class InitializeData:
    """
    A class to handle the creation of initial data for the tables in database.
    """

    def create_initial_data(self, db_connection):
        self.users(db_connection)
        self.twits(db_connection)
        self.follows(db_connection)
        self.likes(db_connection)

    def users(self, db_connection):
        users = InitialUsers.users
        try:
            cursor = db_connection.cursor()
            cursor.executemany("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", users)
            db_connection.commit()
        except Exception as e:
            print(f"An error occurred while adding users: {e}")

    def twits(self, db_connection):
        twits = InitialTwits.tweets
        try:
            cursor = db_connection.cursor()
            cursor.executemany("INSERT INTO twits (user_id, content) VALUES (?, ?)", twits)
            db_connection.commit()
        except Exception as e:
            print(f"An error occurred while adding twits: {e}")

    def follows(self, db_connection):
        follows = InitialFollows.follows
        try:
            cursor = db_connection.cursor()
            cursor.executemany("INSERT INTO follows (follower_id, being_followed_id) VALUES (?, ?)", follows)
            db_connection.commit()
        except Exception as e:
            print(f"An error occurred while adding follows: {e}")

    def likes(self, db_connection):
        likes = InitialLikes.likes
        try:
            cursor = db_connection.cursor()
            cursor.executemany("INSERT INTO likes (user_id, twit_id) VALUES (?, ?)", likes)
            db_connection.commit()
        except Exception as e:
            print(f"An error occurred while adding likes: {e}")


class InitialUsers:
    users = [
        ('water_monk', 'water','water@temple.com'),
        ('earth_monk', 'earth','earth@temple.com'),
        ('fire_monk', 'fire','fire@temple.com'),
        ('air_monk', 'air','air@temple.com'),
        ('avatar', 'unity', 'avatar@spiritual_realm.com')
    ]

class InitialTwits:
    tweets = [
        (1, 'water is awesome!'),
        (2, 'earth is awesome!'),
        (3, 'fire is awesome!'),
        (4, 'air is awesome!'),
        (5, 'let us all coexist!')
    ]

class InitialFollows:
    follows = [
        (1, 2),
        (1, 4),
        (1, 5),
        (2, 1),
        (2, 3),
        (2, 5),
        (3, 2),
        (3, 4),
        (3, 5),
        (5, 1),
        (5, 2),
        (5, 3),
        (5, 4)
    ]

class InitialLikes:
    likes = [
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 5),
        (2, 1),
        (2, 2),
        (2, 3),
        (2, 5),
        (3, 1),
        (3, 2),
        (3, 3),
        (3, 5),
        (4, 4),
        (5, 1),
        (5, 2),
        (5, 3),
        (5, 4),
        (5, 5)
    ]