import sqlite3

connection = sqlite3.connect('database.db') 
cursor = connection.cursor()

class post:
    def __init__(self, url, post_title, ia_answer, post_number, post_month):
        self.url = url
        self.post_title = post_title
        self.ia_answer = ia_answer
        self.post_number = post_number
        self.post_month = post_month    

cursor.execute("""
CREATE TABLE IF NOT EXISTS post (
    URL TEXT,
    POST_TITLE TEXT,
    IA_AWNSER TEXT,
    POST_NUMBER INTEGER,
    POST_MONTH TEXT
    ) 
    """)

#cursor.execute("""
# INSERT INTO post (FIRST_URL, POST_TITLE, IA_AWNSER)
# VALUES ('https://example.com', 'Example Title', 'This is an example answer.')
#""")

connection.commit()
connection.close()
#aa