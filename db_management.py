import csv

def create_database(table_name, cursor):

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            FEUILLET INTEGER, 
            RANG INTEGER,
            XDOMI INTEGER,
            YDOMI INTEGER,
            SDOMI100 INTEGER,
            REGDOMI8 INTEGER,
            PERSLOGI INTEGER,
            AUTOLOGI INTEGER,
            AGE INTEGER,
            SEXE INTEGER,
            P_STATUT INTEGER,
            PERMIS INTEGER,
            P_MOBIL INTEGER,
            NODEPLAC INTEGER,
            HREDE INTEGER,
            MOTIF INTEGER,
            SORIG100 INTEGER,
            REGORIG8 INTEGER,
            SDEST100 INTEGER,
            REGDEST8 INTEGER,
            FACPER REAL,
            F_MENAGE TEXT,
            F_PERS TEXT
    )
""")
    

def insert_csv(csv_file, table_name, cursor):

    with open(csv_file, 'r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            cursor.execute(f'INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', row)
