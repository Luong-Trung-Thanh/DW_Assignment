def insertDataFile(connection,dataFile):
  status = dataFile.status
  description = dataFile.description
  rowCount = dataFile.rowCount
  dataConfigID = dataFile.data_config_id

  mycursor = connection.cursor()
  sql = "INSERT INTO data_files (statues, description, row_count, data_config_id) VALUES (%s, %s, %s, %s)"
  val = (status,description,rowCount,dataConfigID)
  try:
    mycursor.execute(sql, val)
    connection.commit()
  except Exception:
    print("Inserting Data File failed! ",description)
    return -1

  return mycursor.lastrowid

def updateStatusDataFile(connection,dataFile):
  mycursor = connection.cursor()
  sql = "UPDATE data_files SET statues = %s WHERE id = %s"

  val = (dataFile.status, dataFile.id)
  try:
    mycursor.execute(sql, val)
    connection.commit()
  except Exception:
    print("Update Data File Status failed where data_config_id = ",str(dataFile.data_config_id))
    return False

  return True