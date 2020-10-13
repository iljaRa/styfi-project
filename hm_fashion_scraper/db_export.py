#!/usr/bin/python

# /* ------------------ IMPORTS --------------------*/
# /* -----------------------------------------------*/
import mysql.connector as ms


db = ms.connect(
	host = "localhost",
	user = "root",
	passwd = " ",
	database = "fashion_hm"
)

cursor = db.cursor()

def check_if_table_exists():
	cursor.execute("SHOW TABLES LIKE 't_shirts'")
	output = cursor.fetchall()
	if len(output) == 0:
		return False
	else:
		return True

def create_t_shirt_table():
	if not check_if_table_exists():
		cursor.execute("CREATE TABLE t_shirts( \
			t_shirt_id VARCHAR(255) NOT NULL, \
			url VARCHAR(2083) NOT NULL, \
			image_path VARCHAR(1020) NOT NULL, \
			item_name VARCHAR(1020) DEFAULT 'T-Shirt with no name', \
			shop VARCHAR(255) NOT NULL, \
			gender CHAR(1) DEFAULT 'F', \
			price DECIMAL(5,2), \
			created_at TIMESTAMP DEFAULT NOW() ON UPDATE NOW(), \
			PRIMARY KEY (t_shirt_id) \
		)")
	else:
		print('Table t_shirts already exists!')
	
def desc_t_shirts():
	cursor.execute("DESC t_shirts")
	print_db_output()

def print_db_output():
	output = cursor.fetchall()

	for element in output:
		print(element)
   
def insert_into_t_shirts(t_shirt_id, url, image_path, item_name, shop, gender, price):
	query = "INSERT INTO t_shirts (t_shirt_id, url, image_path, item_name, shop, gender, price) \
			VALUES (%s, %s, %s, %s, %s, %s, %s)"
			
	values = (t_shirt_id, url, image_path, item_name, shop, gender, price)
	
	cursor.execute(query, values)
	
	db.commit()

   
def select_all_from_t_shirts():
	cursor.execute("SELECT * FROM t_shirts")
	print_db_output()

def drop_t_shirt_table():
	cursor.execute("DROP TABLE t_shirts")
