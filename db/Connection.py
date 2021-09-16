import mysql.connector

# @description get connection to database
# @return connection
# @author Thanh Luong (thanh.luong@ecepvn.org)
def getConnection(dbName):
  return mysql.connector.connect(
    host="localhost",
    user="root",
    password="MaiThanh@%)$99",
    database=dbName
)

