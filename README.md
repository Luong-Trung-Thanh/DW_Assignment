 
# DW_Assignment
A simple python projects about ETL in DataWarehouse

Project implements the process of download data from open source data and then extract, tranform and load data to data warehouse.

Open source data (article): Vnexpress, CNN,... 

## Get Started
### System requirements
    Python >= 3.5
    Database: MySQL
### Steps To Follow

- For example, run this command inside your terminal:
    ```bash
    git clone https://github.com/Luong-Trung-Thanh/DW_Assignment.git
    ```
- Install file requirement.txt
     ```bash
    pip install requirements.txt
    ```
- Set up database in folder [database.](https://github.com/Luong-Trung-Thanh/DW_Assignment/database) in project
## Sample code

- Here is a sample code that you can run on your machine after having installed project:
    ```bash
        def main():
            # print(checkSize("http://www.ted.com"))
            configID = 4 #form database.db_control.data_file_config
            # fetch data from website, convert to csv file
            dataFile = ScrapeData.fetchArticles(configID)
            # load data from csv to table "article" in "db_warehouse" dababase
            # ArticleDAO.loadDataFromCSVFile2DB()
            # transform data
            TransFormData.transfrom(dataFile);
            # load data
            LoadData.load(dataFile);
        if __name__ == '__main__':
            # checkSize("http://cnn.com")
            # schedule
            # # schedule.every().monday.at("18:00").do(main)
            # schedule.every(1).minutes.do(main)
            # while True:
            #     schedule.run_pending()
            #     time.sleep(1)
            # run immedietly
            main()
    ```