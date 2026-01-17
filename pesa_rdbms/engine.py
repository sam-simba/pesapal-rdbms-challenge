from tables import Table

class DatabaseEngine:
    def __init__(self):
        self.tables = {}
        self.create_default_tables()

    def create_default_tables(self):
        # Merchants table
        merchants_columns = {
            "merchant_id": "INT",
            "name": "TEXT",
            "email": "TEXT"
        }
        self.tables["Merchants"] = Table("Merchants", merchants_columns)

        # Transactions table
        transactions_columns = {
            "transaction_id": "INT",
            "merchant_id": "INT",
            "amount": "FLOAT",
            "payment_method": "TEXT"
        }
        self.tables["Transactions"] = Table("Transactions", transactions_columns)

    def execute(self, command: str):
        # Very basic parser placeholder for demo
        tokens = command.strip().split()
        if len(tokens) == 0:
            return "No command entered"

        cmd = tokens[0].upper()

        if cmd == "SELECT":
            table_name = tokens[-1].rstrip(";")
            if table_name in self.tables:
                return self.tables[table_name].select_all()
            return f"Table {table_name} does not exist"
        
        # INSERT support
        if cmd == "INSERT":
            table_name = tokens[2]
            if table_name not in self.tables:
                return f"Table {table_name} does not exist"

            # Get values inside parentheses
            start = command.find("(")
            end = command.find(")")
            if start == -1 or end == -1:
                return "Syntax error: missing parentheses"

            values_str = command[start+1:end]
            # Split by comma and strip spaces/quotes
            values = [v.strip().strip('"').strip("'") for v in values_str.split(",")]

            # Convert numbers if column type is INT or FLOAT
            table = self.tables[table_name]
            converted_values = []
            for (col_name, col_type), value in zip(table.columns.items(), values):
                if col_type == "INT":
                    value = int(value)
                elif col_type == "FLOAT":
                    value = float(value)
                converted_values.append(value)

            return table.insert(converted_values)

    
        # UPDATE support
        if cmd == "UPDATE":
            table_name = tokens[1]
            if table_name not in self.tables:
                return f"Table {table_name} does not exist"

            # Use uppercase only to detect keywords
            command_upper = command.upper()
            if "SET" not in command_upper or "WHERE" not in command_upper:
                return "Syntax error: missing SET or WHERE"

            # Extract SET and WHERE parts preserving original case for values
            set_part = command[command_upper.find("SET")+3 : command_upper.find("WHERE")].strip()
            where_part = command[command_upper.find("WHERE")+5 : ].strip().rstrip(";")

            # Parse SET clause
            if "=" not in set_part:
                return "Syntax error in SET clause"
            col_name, new_value = [x.strip() for x in set_part.split("=")]
            new_value = new_value.strip('"').strip("'")

            # Parse WHERE clause (only supports equality)
            if "=" not in where_part:
                return "Syntax error in WHERE clause"
            where_col, where_val = [x.strip() for x in where_part.split("=")]
            where_val = where_val.strip('"').strip("'")

            # Find the table
            table = self.tables[table_name]

            # Update rows
            count = 0
            for i, row in enumerate(table.rows):
                row_dict = {col: val for col, val in zip(table.columns.keys(), row)}
                
                # Convert where_val to the proper type based on the column
                col_index = list(table.columns.keys()).index(where_col)
                col_type = list(table.columns.values())[col_index]
                if col_type == "INT":
                    where_val_converted = int(where_val)
                elif col_type == "FLOAT":
                    where_val_converted = float(where_val)
                else:
                    where_val_converted = where_val  # keep string as-is

                col_names = list(table.columns.keys())
                col_index_where = col_names.index(where_col)
                if row[col_index_where] == where_val_converted:
                    # Update the correct column
                    col_index = list(table.columns.keys()).index(col_name)
                    col_type = list(table.columns.values())[col_index]
                    if col_type == "INT":
                        row[col_index] = int(new_value)
                    elif col_type == "FLOAT":
                        row[col_index] = float(new_value)
                    else:
                        row[col_index] = new_value
                    table.rows[i] = row
                    count += 1

            return f"{count} row(s) updated"
        

        
        # DELETE support
        if cmd == "DELETE":
            if len(tokens) < 3:
                return "Syntax error: missing table name"

            table_name = tokens[2]  # DELETE FROM TableName
            table = self.tables.get(table_name)
            if not table:
                return f"Table {table_name} does not exist"

            # extract WHERE clause (everything after WHERE, remove ending semicolon)
            where_index = command.upper().find("WHERE")
            if where_index == -1:
                return "Syntax error: missing WHERE clause"

            where_part = command[where_index + len("WHERE"):].strip().rstrip(";")

            if "=" not in where_part:
                return "Syntax error in WHERE clause"

            where_col, where_val = [x.strip() for x in where_part.split("=")]
            where_val = where_val.strip('"').strip("'")

            # get column index and type
            col_names = list(table.columns.keys())
            col_index_where = col_names.index(where_col)
            col_type = list(table.columns.values())[col_index_where]

            # convert value to proper type
            if col_type == "INT":
                where_val_converted = int(where_val)
            elif col_type == "FLOAT":
                where_val_converted = float(where_val)
            else:
                where_val_converted = where_val

            # delete matching rows
            original_count = len(table.rows)
            table.rows = [r for r in table.rows if r[col_index_where] != where_val_converted]
            deleted_count = original_count - len(table.rows)

            return f"{deleted_count} row(s) deleted"
        return "Command not recognized"
