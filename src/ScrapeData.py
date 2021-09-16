import newspaper
from datetime import datetime
from bs4 import BeautifulSoup
import main
from bean.DataFile import DataFile
import csv
import db.Connection as Con
from bean.DataLog import DataLog
from dao import DataFileDAO, DataLogDAO, DataFileConfigDAO
import pathlib
rootPath = pathlib.Path(__file__).parent
dbControlConnection = Con.getConnection('db_control')


# @description fetch articles from newspaper website
# @return DataFile object
# @author Thanh Luong (thanh.luong@ecepvn.org)
def fetchArticles(configID):
    dataFileConfig = DataFileConfigDAO.getConfigRow(configID)
    # get paper
    paper = newspaper.build(dataFileConfig.url, memoize_articles=False)
    # insert row to "data_file" table in "db_control" database
    dataFile = DataFile(status="DOWNLOADING", name = dataFileConfig.name+"_"+getCurrentDateTime()+"."+dataFileConfig.formatFile,
                        description=paper.description, rowCount=-1,data_config_id=dataFileConfig.id)
    dataFileID = DataFileDAO.insertDataFile(dataFile)

    # set dataFile ID
    dataFile.id = dataFileID

    # write data to csv file
    try:
        writeData2CSVFile(paper.articles, dataFileConfig, dataFile)
    except Exception:
        dataFile.status = "DOWNLOAD FAILED"
        DataFileDAO.updateStatusDataFile(dataFile)


    # update status datafile by id
    dataFile.status = "ER"
    DataFileDAO.updateStatusDataFile(dataFile)
    return dataFile

# @description write article data got from newspaper website to csv file
# @return void
# @author Thanh Luong (thanh.luong@ecepvn.org)
def writeData2CSVFile(articles,dataFileConfig,dataFile):
    row_count = 0
    delimiter = dataFileConfig.separators
    filePath = str(main.rootPath)+"/data/"+dataFile.name
    # create or open csv file to write data
    csvFile = open(filePath, mode="w+", encoding='UTF8', newline='')
    writer = csv.writer(csvFile, delimiter=delimiter)
    # get column names
    columns = getColumns(dataFileConfig)
    # write header for csv file
    writer.writerow(columns)

    # fetch single article and write it's data to file
    for article in articles:
        try:
            print("Downloading "+str(article.url))
            article.download()
            article.parse()
            print("Successful download " + str(article.url))
        except newspaper.article.ArticleException:
            # inform writing row to csv file failed to "data_logs" table
            dataLog = DataLog(description="FAILED to download Article form url: " + str(article.url), name="Download Article")
            DataLogDAO.insertDataLog(dataLog)
            continue

        url = article.url
        title = article.title
        publish_date = getPublishDate(article)
        authors = getAuthors(article)

        # check if has missing data?
        if(publish_date is None or authors is None or str(publish_date).isspace() or str(authors).isspace() or
                str(publish_date).find("[]") >= 0 or str(authors).find("[]") >= 0):
            # inform writing row to csv file failed to "data_logs" table
            print("Failed write to csv " + str(article.url))
            dataLog = DataLog(description="FAILED to write Article form url: " + str(article.url),
                              name="Download Article")
            DataLogDAO.insertDataLog(dataLog)
            continue

        # write to file as row
        rowData = []
        rowData.append(url)
        rowData.append(title)
        rowData.append(publish_date)
        rowData.append(authors)
        writer.writerow(rowData)

        # update row_count
        row_count += 1
        # inform writing row to csv file successfully to "data_logs" table
        print("Successful write csv " + str(article.url))
        dataLog = DataLog(description="SUCCESSFULY write data from " + str(article.url), name="Write data to csv")
        DataLogDAO.insertDataLog( dataLog)

    # after finishing writing, close the file
    csvFile.close()
    # update row_count in dataFile
    dataFile.rowCount = row_count
    DataFileDAO.updateRowCountDataFile(dataFile)



# @description extract publish date from article
# @return publish date (string)
# @author Thanh Luong (thanh.luong@ecepvn.org)
def getPublishDate(article):
    soup = BeautifulSoup(article.html, 'html.parser')
    try:
         article.publish_date = soup.find_all("span", class_="date")[0].text.strip()
    except Exception:
        return article.publish_date
        print("Exception: ", "Can't get publish date")
    return article.publish_date

# @description extract authors from article
# @return authors (string)
# @author Thanh Luong (thanh.luong@ecepvn.org)
def getAuthors(article):
    soup = BeautifulSoup(article.html, 'html.parser')
    try:
        listData = soup.find_all('p', attrs={'style': 'text-align:right;'})
        if (len(listData) <= 0):
            listData = soup.find_all("p", class_="author_mail")
        elif (len(listData) <= 0):
            listData = soup.find_all("p", class_="Normal")

        article.authors = listData[len(listData) - 1].text.strip()
        return article.authors
    except Exception:
        return article.authors
        print("Exception: ", "Can't get authors")

# @description get current datetime, "%Y-%m-%d_%H-%M-%S" format. Ex: 2021-09-16_10-27-26
# @return string
# @author Thanh Luong (thanh.luong@ecepvn.org)
def getCurrentDateTime():
    # datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d_%H-%M-%S")
    return dt_string




# @description # get the list of columns from columns string, split by ",", ex: url, title, publish_date, authors
# => ['url', 'title', 'publish_date', 'authors']
# @return list of columns
# @author Thanh Luong (thanh.luong@ecepvn.org)
def getColumns(dataFileConfig):
    # get columns string from data_file_config
    columnsString = dataFileConfig.columns

    columnsList = columnsString.rsplit(",")
    return columnsList


