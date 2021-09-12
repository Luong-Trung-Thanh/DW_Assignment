import mysql.connector
import time
from datetime import datetime
import schedule

def getConnection(dbName):
  return mysql.connector.connect(
    host="localhost",
    user="root",
    password="MaiThanh@%)$99",
    database=dbName
)

# if __name__ == '__main__':
#   schedule.every(10).seconds.do(run)
#   while True:
#     # Checks whether a scheduled task
#     # is pending to run or not
#     schedule.run_pending()
#     time.sleep(1)