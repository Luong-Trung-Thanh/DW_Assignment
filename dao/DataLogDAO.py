import db.Connection as Con

dbControlConnection = Con.getConnection('db_control')

# @description insert data log to "data_logs" table in "db_control" database
# @return boolean
# @author Thanh Luong (thanh.luong@ecepvn.org)
def insertDataLog(dataLog):
  name = dataLog.name
  description = dataLog.description

  mycursor = dbControlConnection.cursor()
  sql = "INSERT INTO data_logs (name, description) VALUES (%s, %s)"
  val = (name,description)
  try:
    mycursor.execute(sql, val)
    dbControlConnection.commit()
  except Exception:
    print("Inserting Data Log failed! ",description)
    return False
  return True