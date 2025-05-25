import sys

from dataclasses import dataclass

# import sqlparse - available if you need it!

database_file_path = sys.argv[1]
command = sys.argv[2]

if command == ".dbinfo":
    with open(database_file_path, "rb") as database_file:
        # You can use print statements as follows for debugging, they'll be visible when running tests.
        print("Logs from your program will appear here!", file=sys.stderr)

        # Uncomment this to pass the first stage
        database_file.seek(16)  # Skip the first 16 bytes of the header
        page_size = int.from_bytes(database_file.read(2), byteorder="big")
        database_file.seek(103)
        num_of_tables = int.from_bytes(database_file.read(2), byteorder="big")

        print(f"database page size: {page_size}")
        print(f"number of tables: {num_of_tables}")
elif command == ".tables":
    with open(database_file_path, "rb") as database_file:
        database_file.seek(103)
        num_of_tables = int.from_bytes(database_file.read(2), byteorder="big")
        table_names = []
        start_seek = 108
        for i in range(0, num_of_tables):
            database_file.seek(start_seek)
            pointer = int.from_bytes(database_file.read(2), byteorder="big")
            #print("pointer", hex(pointer))
            database_file.seek(pointer + 2)

            len_of_header = int.from_bytes(database_file.read(1), byteorder="big")
            #print("len header", len_of_header, hex(len_of_header))

            database_file.seek(pointer + 3)
            len_of_type = int.from_bytes(database_file.read(1), byteorder="big")
            #print("len type", len_of_type, hex(len_of_type))
            len_of_type = (int)((len_of_type - 13) / 2)
            #print(len_of_type)

            database_file.seek(pointer + 4)
            len_of_name = int.from_bytes(database_file.read(1), byteorder="big")
            #print("len name", len_of_name, hex(len_of_name))
            len_of_name = (int)((len_of_name - 13) / 2)
            #print(len_of_name)

            database_file.seek(pointer + 5)
            len_of_tablename = int.from_bytes(database_file.read(1), byteorder="big")
            #print("len tablename", len_of_tablename, hex(len_of_tablename))
            len_of_tablename = (int)((len_of_tablename - 13) / 2)
            #print(len_of_tablename)

            database_file.seek(pointer + 2 + len_of_header + len_of_type + len_of_name)
            #table_name = hex(int.from_bytes(database_file.read(1), byteorder="big"))
            table_name = database_file.read(len_of_tablename).decode("utf-8")
            if table_name != "sqlite_sequence":
                table_names.append(table_name)
            
            start_seek += 2
        table_names = ' '.join(table_names)
        print(table_names)
else:
    print(f"Invalid command: {command}")
