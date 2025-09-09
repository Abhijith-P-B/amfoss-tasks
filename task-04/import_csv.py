import mysql.connector
import csv
db = mysql.connector.connect(host = "localhost", user = "root", passwd = "root", database = "CineScope")
if db.is_connected():
    print("Connection to database successfull !")
    cursor = db.cursor()
    cursor.execute("create table MovieRecords(Series_Title varchar(200),Released_Year int NULL,Genre varchar(100),IMDB_Rating float NULL,Director varchar(100),Star1 varchar(100),Star2 varchar(100),Star3 varchar(100))")
    file = open("movies.csv","r")
    reader = csv.reader(file)
    next(reader)
    for x in reader:
        if x[1].strip() == '':
            year = None
        else:
            year = int(x[1].strip())
        if x[3].strip() == '':
            rating = None
        else:
            rating = float(x[3].strip())
        insert = "insert into MovieRecords(Series_Title,Released_Year,Genre,IMDB_Rating,Director,Star1,Star2,Star3) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(insert,(x[0],year,x[2],rating,x[4],x[5],x[6],x[7]))
    db.commit()
    file.close()
    print("Movie records added succesfully to the database !")
else:
    print("Connection to database failed !")