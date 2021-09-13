
import newspaper

from bs4 import BeautifulSoup
from newspaper import Article

import main
from bean.DataFile import DataFile
import csv
import db.Connection as Con
from bean.DataLog import DataLog
from dao import DataFileDAO, DataLogDAO
import pathlib
rootPath = pathlib.Path(__file__).parent
dbControlConnection =  Con.getConnection('db_control')
dbWarehouseConnection = Con.getConnection('db_warehouse')




# use beautiful soup library to extract data from html page
# article = Article("http://www.ted.com/talks/katie_mack_the_mind_bending_reality_of_the_universe")
# article.download()
# article.parse()
# print(article.publish_date)
# print(type(article.publish_date))
# print(article.publish_date is None)

# soup = BeautifulSoup(article.html, 'html.parser')
# print(soup.prettify())
# print(soup.find_all("div", class_="normal")[0].text)


def fetchArticles(dataFileConfig):
    # get paper
    paper = newspaper.build(dataFileConfig.url, memoize_articles=False)
    # insert row to "data_file" table in "db_control" database
    dataFile = DataFile(status="running", description=paper.description, rowCount=paper.size(),data_config_id=dataFileConfig.id)
    DataFileDAO.insertDataFile(dbControlConnection,dataFile)
    # write data to csv file
    writeData2CSVFile(paper.articles,dataFileConfig)

    dataFile.status = "finished"
    DataFileDAO.updateStatusDataFile(dbControlConnection,dataFile)



def writeData2CSVFile(articles,dataFileConfig):
    delimiter = dataFileConfig.separators

    filePath = str(main.rootPath)+"/"+dataFileConfig.pathFileDes + "." + dataFileConfig.formatFile
    # create or open csv file to write data
    csvFile = open(filePath, mode="w+", encoding='UTF8', newline='')
    writer = csv.writer(csvFile, delimiter=delimiter)
    # write header for file
    writer.writerow(['url', 'title', 'publish_date', 'authors'])

    # fetch single article and write it's data to file
    for article in articles:
        try:
            print("Downloading "+str(article.url))
            article.download()
            article.parse()
            print("Successful download " + str(article.url))
        except newspaper.article.ArticleException:
            # inform writing row to csv file successfully to "data_logs" table
            dataLog = DataLog(description="Failed to download Article form url: " + str(article.url), name="Download Article")
            DataLogDAO.insertDataLog(dbControlConnection, dataLog)
            continue


        url = article.url
        title = article.title
        publish_date = getPublishDate(article)
        authors = getAuthors(article)
        if(publish_date is None or authors is None):
            # inform writing row to csv file successfully to "data_logs" table
            print("Failed write to csv " + str(article.url))
            dataLog = DataLog(description="Failed to write Article form url: " + str(article.url),
                              name="Download Article")
            DataLogDAO.insertDataLog(dbControlConnection, dataLog)
            continue

        # write to file as row
        writer.writerow([url, title, publish_date, authors])

        # inform writing row to csv file successfully to "data_logs" table
        print("Successful write csv " + str(article.url))
        dataLog = DataLog(description="Successfully write data from " + str(article.url), name="Write data to csv")
        DataLogDAO.insertDataLog(dbControlConnection, dataLog)

    # after finishing writing, close the file
    csvFile.close()

def getPublishDate(article):
    soup = BeautifulSoup(article.html, 'html.parser')
    try:
         article.publish_date = soup.find_all("span", class_="date")[0].text.strip()
    except Exception:
        return article.publish_date
        print("Exception: ", "Can't get publish date")
    return article.publish_date

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

