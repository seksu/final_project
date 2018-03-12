# created by sek su
#!/usr/bin/python

import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","root","654321","faces" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT * FROM account_account")

# Fetch a single row using fetchone() method.
datas = cursor.fetchall()
print("Email : "+datas.id)
count = 0
for data in datas:
    print('count : '+str(count))
    print(data)

# disconnect from server
db.close()
