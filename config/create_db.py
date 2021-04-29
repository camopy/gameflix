import MySQLdb

print("Connecting...")
conn = MySQLdb.connect(user="camopy", passwd="devdb", host="localhost", port=3306)

# conn.cursor().execute("DROP DATABASE `gameflix`;")
# conn.commit()

create_tables = """SET NAMES utf8;
    CREATE DATABASE `gameflix` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
    USE `gameflix`;
    CREATE TABLE `game` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `name` varchar(50) COLLATE utf8_bin NOT NULL,
      `category` varchar(40) COLLATE utf8_bin NOT NULL,
      `console` varchar(20) NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    CREATE TABLE `user` (
      `id` varchar(8) COLLATE utf8_bin NOT NULL,
      `name` varchar(20) COLLATE utf8_bin NOT NULL,
      `password` varchar(8) COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;"""

conn.cursor().execute(create_tables)

cursor = conn.cursor()
cursor.executemany(
    "INSERT INTO gameflix.user (id, name, password) VALUES (%s, %s, %s)",
    [("paulo", "Paulo Camopy", "123"), ("amanda", "Amanda Magalhaes", "321")],
)

cursor.execute("select * from gameflix.user")
print(" -------------  Users:  -------------")
for user in cursor.fetchall():
    print(user[1])

cursor.executemany(
    "INSERT INTO gameflix.game (name, category, console) VALUES (%s, %s, %s)",
    [
        ("God of War 4", "Action", "PS4"),
        ("NBA 2k18", "Sport", "Xbox One"),
        ("Rayman Legends", "Indie", "PS4"),
        ("Super Mario RPG", "RPG", "SNES"),
        ("Super Mario Kart", "Race", "SNES"),
        ("Fire Emblem Echoes", "Strategy", "3DS"),
    ],
)

cursor.execute("select * from gameflix.game")
print(" -------------  Games:  -------------")
for game in cursor.fetchall():
    print(game[1])

conn.commit()
cursor.close()