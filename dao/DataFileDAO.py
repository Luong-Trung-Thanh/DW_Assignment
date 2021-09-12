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
    return False
  print(mycursor.rowcount, "was inserted.")
  return True