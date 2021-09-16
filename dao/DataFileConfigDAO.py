from bean.DataFileConfig import DataFileConfig
import db.Connection as Con

dbControlConnection =  Con.getConnection('db_control')
dbStagingConnection = Con.getConnection('db_staging')

# @description get data file config row by ID
# @return DataFileConfig object
# @author Thanh Luong (thanh.luong@ecepvn.org)
def getConfigRow(configID):
    mycursor = dbControlConnection.cursor()
    sql = "SELECT * FROM data_file_config WHERE id =%s"
    arg = (configID,)
    mycursor.execute(sql,arg)

    myresult = mycursor.fetchall()
    try:
        firstRow = myresult[0]
        dataFileConfig = DataFileConfig(id=firstRow[0], url=firstRow[1], name=firstRow[2], description=firstRow[3],
                                        columns=firstRow[4], separators=firstRow[5],formatFile=firstRow[6],
                                        destination=firstRow[7], createdAt=firstRow[8], updatedAt=firstRow[9])
    except Exception:
        print("Exception: " + str(configID)+" id doesn't match any data_file_config's table row.")
        return None
    return dataFileConfig
