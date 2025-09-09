import mysql.connector
import csv
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QGridLayout, 
    QTextEdit, QSizePolicy, QLineEdit
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CineScope – Dashboard")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet("background-color: #121212; color: white; padding: 20px;")
        self.search_mode = None
        self.selected_columns = {"title": False,"year": False,"genre": False,"rating": False,"director": False,"stars": False}
        self.search_buttons_list = []
        self.column_buttons_list = []
        self.init_ui()
        self.db = mysql.connector.connect(host="localhost",user="root",passwd="root",database="CineScope")
        self.cursor = self.db.cursor()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        # Header
        header = QLabel("🎬 CineScope Dashboard")
        header.setFont(QFont("Arial", 24, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setFixedHeight(80)
        main_layout.addWidget(header)

        split_layout = QHBoxLayout()

        # Left Panel
        left_container = QVBoxLayout()
        left_container.setSpacing(10)
        left_container.setAlignment(Qt.AlignTop)

        # Search buttons
        search_heading = QLabel("Search By")
        search_heading.setFont(QFont("Arial", 18, QFont.Bold))
        left_container.addWidget(search_heading)

        search_buttons = [
            ("Genre", "genre"),
            ("Year", "year"),
            ("Rating", "rating"),
            ("Director", "director"),
            ("Actor", "actor"),
        ]

        search_grid = QGridLayout()
        for index, (label, mode) in enumerate(search_buttons):
            btn = QPushButton(label)
            btn.setStyleSheet(self.get_button_style(False))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.clicked.connect(lambda _, m=mode, b=btn: self.set_search_mode(m, b))
            row, col = divmod(index, 2)
            search_grid.addWidget(btn, row, col)
            self.search_buttons_list.append(btn)
        left_container.addLayout(search_grid)

        # Column selection
        column_heading = QLabel("Select Columns")
        column_heading.setFont(QFont("Arial", 18, QFont.Bold))
        left_container.addWidget(column_heading)

        column_buttons = [
            ("Title", "title"),
            ("Year", "year"),
            ("Genre", "genre"),
            ("Rating", "rating"),
            ("Director", "director"),
            ("Stars", "stars"),
        ]

        self.column_grid = QGridLayout()
        for index, (label, col) in enumerate(column_buttons):
            btn = QPushButton(label)
            btn.setStyleSheet(self.get_button_style(False))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.clicked.connect(lambda _, c=col, b=btn: self.toggle_column(c, b))
            row, col = divmod(index, 2)
            self.column_grid.addWidget(btn, row, col)
            self.column_buttons_list.append(btn)
        left_container.addLayout(self.column_grid)

        # Search input
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Enter search term")
        self.query_input.setStyleSheet("background-color: #1e1e1e; color: white; padding: 5px; border: 1px solid #444;")
        left_container.addWidget(self.query_input)

        # Action buttons
        action_layout = QHBoxLayout()
        search_btn = QPushButton("Search")
        search_btn.setStyleSheet("background-color: #e50914; color: white; padding: 6px; border-radius: 5px;")
        search_btn.clicked.connect(self.execute_search)
        action_layout.addWidget(search_btn)

        export_btn = QPushButton("Export CSV")
        export_btn.setStyleSheet("background-color: #1f1f1f; color: white; padding: 6px; border-radius: 5px;")
        export_btn.clicked.connect(self.export_csv)
        action_layout.addWidget(export_btn)
        left_container.addLayout(action_layout)

        # Right Panel
        right_side_layout = QVBoxLayout()
        right_side_layout.setSpacing(10)

        # Table
        self.table = QTableWidget()
        self.table.setStyleSheet("""
            QTableWidget {
                color: white;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: white;
                color: black;
                padding: 4px;
            }
        """)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Output console
        self.output_console = QTextEdit()
        self.output_console.setPlaceholderText("Results will appear here...")
        self.output_console.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: white;
                border: 1px solid #444;
                padding: 5px;
            }
        """)
        self.output_console.setFixedHeight(100)

        right_side_layout.addWidget(self.table)
        right_side_layout.addWidget(self.output_console)

        split_layout.addLayout(left_container, 2)
        split_layout.addLayout(right_side_layout, 8)
        main_layout.addLayout(split_layout)
        self.setLayout(main_layout)

    def get_button_style(self, is_selected):
        if is_selected:
            return "QPushButton {background-color: #ffcc00; border: 1px solid #ff9900; border-radius: 3px; padding: 6px;}"
        else:
            return "QPushButton {background-color: #1f1f1f; border: 1px solid #333; border-radius: 3px; padding: 6px;} QPushButton:hover {background-color: #333;}"

    def set_search_mode(self, mode, btn):
        self.search_mode = mode
        for b in self.search_buttons_list:
            b.setStyleSheet(self.get_button_style(False))
        btn.setStyleSheet(self.get_button_style(True))

    def toggle_column(self, column, btn):
        self.selected_columns[column] = not self.selected_columns[column]
        btn.setStyleSheet(self.get_button_style(self.selected_columns[column]))

    def execute_search(self):
        columns = [col for col, selected in self.selected_columns.items() if selected]
        if not columns:
            self.output_console.clear()
            self.output_console.append("Query executed successfully")
            self.output_console.append("SELECT * FROM MovieRecords")
            return

        column_map = {"title": "Series_Title","year": "Released_Year","genre": "Genre","rating": "IMDB_Rating","director": "Director","stars": "CONCAT(Star1, ' ', Star2, ' ', Star3)","actor": "CONCAT(Star1, ' ', Star2, ' ', Star3)"}
        selected_cols = ", ".join([column_map[c] for c in columns])
        sql = "SELECT " + selected_cols + " FROM MovieRecords"
        query_text = self.query_input.text().strip()
        final_sql = sql
        if query_text and self.search_mode:
            db_column = column_map[self.search_mode]
            if self.search_mode == "actor":
                sql += " WHERE Star1 LIKE %s OR Star2 LIKE %s OR Star3 LIKE %s"
                self.cursor.execute(sql, ("%" + query_text + "%", "%" + query_text + "%", "%" + query_text + "%"))
                final_sql += f" WHERE Star1 LIKE '%{query_text}%' OR Star2 LIKE '%{query_text}%' OR Star3 LIKE '%{query_text}%'"
            else:
                sql += " WHERE " + db_column + " LIKE %s"
                self.cursor.execute(sql, ("%" + query_text + "%",))
                final_sql += f" WHERE {db_column} LIKE '%{query_text}%'"
        else:
            self.cursor.execute(sql)

        rows = self.cursor.fetchall()
        self.table.setRowCount(0)
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        for row_idx, row_data in enumerate(rows):
            self.table.insertRow(row_idx)
            for col_idx, data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

        self.output_console.clear()
        self.output_console.append("Query executed successfully")
        self.output_console.append(final_sql)

    def export_csv(self):
        f = open("exported_movies.csv", "w", newline="")
        writer = csv.writer(f)
        headers = [self.table.horizontalHeaderItem(col).text() for col in range(self.table.columnCount())]
        writer.writerow(headers)
        for row in range(self.table.rowCount()):
            row_data = [self.table.item(row, col).text() for col in range(self.table.columnCount())]
            writer.writerow(row_data)
        f.close()
        self.output_console.append("Exported to CSV")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec())