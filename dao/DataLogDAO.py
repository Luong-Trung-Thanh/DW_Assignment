import db.Connection as Con

dbControlConnection = Con.getConnection('db_control')
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