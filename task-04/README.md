# Task-04 (CineScope)

## STEP -I
Created the file "import_csv.py" which can:

$ Create a table named "MovieRecords" in the DataBase:"CineScope".

$ Open "movies.csv" and read line by line.

$ Add records into the table "MovieRecords".

## STEP - II
$ The "dashboard.py" was modified to make it work.

$ It was connected to MySQL DataBase by using mysql.connector.

$ The search by part is single selection, that is the user could select only one button and once selected the button
  turns yellow.

$ The select column part is multiple choice selction, where all the selected buttons turn yellow.

$ According to the search by and columns selected, custom queries will be used to print the records accordingly.

## STEP - III
$ The "Export CSV" button exports the current printed records along with the heading row to "exported_movies.csv"

$ Whenever the records was exported, the "exported_movies.csv" is overwritten.

# STEPS TO USE IT IN YOUR SYSTEM :
1. Clone the repository to your system and navigate to it by using:
```bash
gh repo clone Abhijith-P-B/amfoss_praveshan
```
```bash
cd amfoss_praveshan/task-04
```

2. Create a virtual environment and install the required packages listed in file requirements.txt using:
```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```
```bash
pip install -r requirements.txt
```

3. Install and configure a MySQL server on your system.

4. Edit the line 3 in import_csv.py for connecting to your Database using:
```bash
nano import_csv.py
```
   Run import_csv.py to read records from the CSV file and add to your database using:
```bash
python3 import_csv.py
```

5. Also modify the line 23 of dashboard.py for connecting to your Database using:
```bash
nano dashboard.py
```

6. Run main.py, then click "Start Exploring" to generate custom queries and print according to need.
```bash
python3 main.py
```

7. To export the printed output into exported_movies.csv , click "Export to CSV".

