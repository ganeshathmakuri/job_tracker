import mysql.connector
conn = mysql.connector.connect(host='localhost', user='root', password='sql password')
print("connected")
conn.close()