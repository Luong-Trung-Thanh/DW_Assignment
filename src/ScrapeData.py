import bs4
import dateutil.utils
import newspaper
from newspaper import Article
from bs4 import BeautifulSoup
from newspaper import news_pool
from bean.DataFileConfig import DataFileConfig
import csv
import bean.DataFileConfig
import db.Connection as Con
from pathlib import Path
import dao.ArticleDAO as ArticleDAO
import dao.DataFileConfigDAO as DataFileConfigDAO
import dao.DataFileDAO as DataFileDAO
from bean.DataFile import DataFile
dbControlConnection =  Con.getConnection('db_control')
dbWarehouseConnection = Con.getConnection('db_warehouse')


cnn_paper = newspaper.build("http://cnn.com",language='en')

# print(cnn_paper.size()) #how many articles cnn has?

# use beautiful soup library to extract data from html page
# article = Article("https://vnexpress.net/ronaldo-tu-choi-de-nghi-roi-san-cua-solskjaer-4355118.html")
# article.download()
# article.parse()
# soup = BeautifulSoup(article.html, 'html.parser')
# print(soup.prettify())
# print(soup.find_all("div", class_="normal")[0].text)


configID = 1;
dataFileConfig = DataFileConfigDAO.getConfigRow(configID)

def fetchArticle(dataFileConfig):
    # get paper
    paper = newspaper.build(dataFileConfig.url, memoize_articles=False)
    # insert row to "data_file" table in "db_control" database
    dataFile = DataFile("running", paper.description, paper.size(),dataFileConfig.id);
    DataFileDAO.insertDataFile(dbControlConnection,dataFile)
    # create or open csv file to write data
    pathFile = dataFileConfig.pathFileDes+"."+dataFileConfig.formatFile
    csvFile = open(pathFile, mode='w+', encoding='UTF8', newline='')
    writer = csv.writer(csvFile, delimiter=dataFileConfig.separators)
    # write header for file
    writer.writerow(['url', 'title', 'publish_date', 'authors'])

    # fetch single article and write it's data to file
    for article in paper.articles:
        article.download()
        article.parse()
        soup = BeautifulSoup(article.html, 'html.parser')

        # try to get publish_date
        try:

            article.publish_date = soup.find_all("span", class_="date")[0].text.strip()
        except Exception:
            print("Exception: ", "Can't get publish date")

        # try to get authors
        try:
            listData = soup.find_all('p', attrs={'style': 'text-align:right;'})
            if(len(listData)<=0):
                listData = soup.find_all("p", class_="author_mail")
            elif(len(listData)<=0):
                listData = soup.find_all("p", class_="Normal")
            article.authors = listData[len(listData) - 1].text.strip()
        except Exception:
            print("Exception: ", "Can't get authors")

        # write to file as row
        writer.writerow([article.url, article.title, article.publish_date, article.authors])
        print(article.url+" has been written")

    # after finish writing, close the file
    csvFile.close()

if __name__ == '__main__':
    # fetch data from website, convert to csv file
    fetchArticle(dataFileConfig)

    # load data from csv to table "article" in "db_warehouse" dababase
    # ArticleDAO.loadDataFromCSVFile2DB(dataFileConfig,dbWarehouseConnection)
