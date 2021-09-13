def insertDataLog(connection,dataLog):
  name = dataLog.name
  description = dataLog.description

  mycursor = connection.cursor()
  sql = "INSERT INTO data_logs (name, description) VALUES (%s, %s)"
  val = (name,description)
  try:
    mycursor.execute(sql, val)
    connection.commit()
  except Exception:
    print("Inserting Data Log failed! ",description)
    return False

  return True