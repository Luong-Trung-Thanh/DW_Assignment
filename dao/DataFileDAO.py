from datetime import datetime
import db.Connection as Con

dbControlConnection = Con.getConnection('db_control')

def insertDataFile(dataFile):
    name = dataFile.name
    status = dataFile.status
    description = dataFile.description
    rowCount = dataFile.rowCount
    dataConfigID = dataFile.data_config_id

    mycursor = dbControlConnection.cursor()
    sql = "INSERT INTO data_files (name, statues, description, row_count, data_config_id) VALUES (%s,%s, %s, %s, %s)"
    val = (name, status, description, rowCount, dataConfigID)
    try:
        mycursor.execute(sql, val)
        dbControlConnection.commit()
    except Exception:
        print("Inserting Data File failed! ", description)
        return -1

    return mycursor.lastrowid


def updateStatusDataFile(dataFile):
    mycursor = dbControlConnection.cursor()
    current_Date = datetime.now()
    formatted_date = current_Date.strftime('%Y-%m-%d %H:%M:%S')

    sql = "UPDATE data_files SET statues = %s, updated_at = %s WHERE id = %s"

    val = (dataFile.status, formatted_date, dataFile.id)
    try:
        mycursor.execute(sql, val)
        dbControlConnection.commit()
    except Exception:
        print("Update Data File Status failed where data file ID = ", str(dataFile.id))
        return False
    return True


def updateRowCountDataFile(dataFile):
    mycursor = dbControlConnection.cursor()
    current_Date = datetime.now()
    formatted_date = current_Date.strftime('%Y-%m-%d %H:%M:%S')
    sql = "UPDATE data_files SET row_count = %s, updated_at = %s WHERE id = %s"

    val = (dataFile.rowCount, formatted_date, dataFile.id)
    try:
        mycursor.execute(sql, val)
        dbControlConnection.commit()
    except Exception:
        print("Update Data File row_count failed where data_config_id = ", str(dataFile.data_config_id))
        return False
    return True


# get data file by status. status can be: ER, TR, LR ,...
# return list of data file with status
def getDataFileByStatus(status):
    mycursor = dbControlConnection.cursor()
    sql = "SELECT * FROM data_files where statues = %s"
    val = (status,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    return myresult

# import db.Connection as Con
# dbControlConnection =  Con.getConnection('db_control')
# dbStagingConnection = Con.getConnection('db_staging')
# if __name__ == '__main__':
#     getDataFileByStatus("ER",dbControlConnection)
