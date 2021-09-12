from bean.DataFileConfig import DataFileConfig
import db.Connection as Con

dbControlConnection =  Con.getConnection('db_control')
dbWarehouseConnection = Con.getConnection('db_warehouse')

def getConfigRow(configID):
    mycursor = dbControlConnection.cursor()
    sql = "SELECT * FROM data_file_config WHERE id =%s"
    arg = (configID,)
    mycursor.execute(sql,arg)

    myresult = mycursor.fetchall()
    try:
        firstRow = myresult[0]
        dataFileConfig = DataFileConfig(firstRow[0], firstRow[1], firstRow[2], firstRow[3], firstRow[4], firstRow[5],
                                        firstRow[6], firstRow[7], firstRow[8], firstRow[9])
    except Exception:
        print("Exception: " + str(configID)+" id doesn't match any data_file_config's table row.")
        return None
    return dataFileConfig


if __name__ == '__main__':
    print(getConfigRow(1).url)