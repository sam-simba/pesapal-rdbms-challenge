import json
import os
from .tables import Table

DB_FILE = "data/db.json"

class DatabaseEngine:
    def __init__(self):
        self.tables = {}
        self.create_default_tables()
        self.load_or_create_db()
    
    def load_or_create_db(self):
        os.makedirs("data", exist_ok=True)

        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r") as f:
                raw = json.load(f)

            for table_name, table_data in raw.items():
                self.tables[table_name] = Table.from_dict(table_name, table_data)

        else:
            self.create_default_tables()
            self.save()
        

    def save(self):
        with open(DB_FILE, "w") as f:
            json.dump(
                {name: table.to_dict() for name, table in self.tables.items()},
                f,
                indent=2
            )


    def left_join(self, left_table, right_table, left_key, right_key):
        result = []

        left_rows = [
            {col: val for col, val in zip(self.tables[left_table].columns.keys(), row)}
            for row in self.tables[left_table].rows
        ]
        right_rows = [
            {col: val for col, val in zip(self.tables[right_table].columns.keys(), row)}
            for row in self.tables[right_table].rows
        ]

        for lrow in left_rows:
            matched = False
            for rrow in right_rows:
                if lrow[left_key] == rrow[right_key]:
                    # Prefix columns with table names to avoid collisions
                    combined = {f"{left_table}.{k}": v for k, v in lrow.items()}
                    combined.update({f"{right_table}.{k}": v for k, v in rrow.items()})
                    result.append(combined)
                    matched = True

            if not matched:
                combined = {f"{left_table}.{k}": v for k, v in lrow.items()}
                # Add right table columns as None
                for col in self.tables[right_table].columns:
                    combined[f"{right_table}.{col}"] = None
                result.append(combined)

        return result

    def get_indexes(self, table_name):
        if table_name not in self.tables:
            return f"Table {table_name} does not exist"
        
        table = self.tables[table_name]
        # Assuming the Table class has an `indexes` attribute
        return table.indexes

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


        # CREATE INDEX support
        if cmd == "CREATE" and len(tokens) > 1 and tokens[1].upper() == "INDEX":
            # Expecting: CREATE INDEX index_name ON TableName (column_name)
            tokens_upper = [t.upper() for t in tokens]

            if "ON" not in tokens_upper:
                return "Syntax error: missing ON"

            on_index = tokens_upper.index("ON")
            if on_index + 1 >= len(tokens):
                return "Syntax error: missing table name after ON"

            table_name = tokens[on_index + 1]
            if table_name not in self.tables:
                return f"Table {table_name} does not exist"

            # Extract column from parentheses
            start = command.find("(")
            end = command.find(")")
            if start == -1 or end == -1:
                return "Syntax error: missing parentheses for column"

            column_name = command[start + 1:end].strip()
            table = self.tables[table_name]
            return table.create_index(column_name)

        #SELECT Support  
        if cmd == "SELECT":
            tokens = command.strip().split()
            tokens_upper = [t.upper() for t in tokens]
            command_upper = command.upper()

            if len(tokens) < 4:
                return "Syntax error in SELECT"

            if tokens_upper[1] != "*":
                return "Syntax error: only SELECT * is supported"

            if "FROM" not in tokens_upper:
                return "Syntax error: missing FROM"

            from_index = tokens_upper.index("FROM")
            left_table = tokens[from_index + 1]
            left_table = tokens[from_index + 1].strip().rstrip(";")

            if left_table not in self.tables:
                return f"Table {left_table} does not exist"

            table = self.tables[left_table]

            # Check for JOIN
            if "JOIN" in tokens_upper:
                join_index = tokens_upper.index("JOIN")
                right_table = tokens[join_index + 1]

                if right_table not in self.tables:
                    return f"Table {right_table} does not exist"

                if "ON" not in tokens_upper:
                    return "Syntax error: missing ON clause"

                on_index = tokens_upper.index("ON")
                on_clause = " ".join(tokens[on_index + 1:])  # everything after ON
                
                try:
                    left_key_raw, right_key_raw = [x.strip() for x in on_clause.split("=")]
                    left_key = left_key_raw.split(".")[-1]  # remove table prefix
                    right_key = right_key_raw.split(".")[-1]
                except:
                    return "Syntax error in ON clause"

                # Call your existing left_join method
                return self.left_join(left_table, right_table, left_key, right_key)

            # WHERE support
            if "WHERE" in command_upper:
                where_part = command[command_upper.index("WHERE") + 5:].strip().rstrip(";")

                if "=" not in where_part:
                    return "Syntax error in WHERE clause"

                where_col, where_val = [x.strip() for x in where_part.split("=", 1)]
                where_val = where_val.strip("'").strip('"')

                col_index = list(table.columns.keys()).index(where_col)
                col_type = list(table.columns.values())[col_index]

                if col_type == "INT":
                    where_val = int(where_val)
                elif col_type == "FLOAT":
                    where_val = float(where_val)

                return [
                    dict(zip(table.columns.keys(), row))
                    for row in table.rows
                    if row[col_index] == where_val
                ]

            return table.select_all()



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
            user_values = [v.strip().strip('"').strip("'") for v in values_str.split(",")]

            # Get table
            table = self.tables[table_name]

            # Auto-increment ID for the first column
            id_col_index = 0
            if table.rows:
                next_id = max(row[id_col_index] for row in table.rows) + 1
            else:
                next_id = 1

            # Make sure number of user values matches remaining columns
            if len(user_values) != len(table.columns) - 1:
                return f"Error: expected {len(table.columns)-1} values, got {len(user_values)}"

            # Prepare converted values
            converted_values = [next_id]  # first column is ID
            for i, (col_name, col_type) in enumerate(list(table.columns.items())[1:]):  # skip first column
                value = user_values[i]
                if col_type == "INT":
                    value = int(value)
                elif col_type == "FLOAT":
                    value = float(value)
                converted_values.append(value)

            if table_name == "Merchants":
                email_index = list(table.columns.keys()).index("email")
                if any(r[email_index] == converted_values[email_index] for r in table.rows):
                    return f"Error: email '{converted_values[email_index]}' already exists"
            
            # After preparing converted_values but before inserting
            if table_name == "Transactions":
                # Find the merchant_id column in Transactions
                merchant_id_index = list(table.columns.keys()).index("merchant_id")
                merchant_id_value = converted_values[merchant_id_index]

                # Check if this merchant exists
                merchant_table = self.tables.get("Merchants")
                merchant_exists = any(
                    r[list(merchant_table.columns.keys()).index("merchant_id")] == merchant_id_value
                    for r in merchant_table.rows
                )

                if not merchant_exists:
                    return f"Error: You can only insert transactions for existing merchants. Merchant with ID {merchant_id_value} does not exist"


            result = table.insert(converted_values)
            self.save()
            return result 


    

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
            
            self.save()
            return f"{count} row(s) updated"
        

        
        # DELETE support
        if cmd == "DELETE":
            table_name = tokens[2]  # DELETE FROM TableName ...
            if table_name not in self.tables:
                return f"Table {table_name} does not exist"

            command_upper = command.upper()
            if "WHERE" not in command_upper:
                return "Syntax error: missing WHERE clause"

            # Extract WHERE clause preserving original case
            where_part = command[command_upper.find("WHERE")+5 : ].strip().rstrip(";")

            if "=" not in where_part:
                return "Syntax error in WHERE clause"

            where_col, where_val = [x.strip() for x in where_part.split("=")]
            where_val = where_val.strip('"').strip("'")

            # Find the table
            table = self.tables[table_name]

            # Convert WHERE value to proper type
            col_index = list(table.columns.keys()).index(where_col)
            col_type = list(table.columns.values())[col_index]
            if col_type == "INT":
                where_val_converted = int(where_val)
            elif col_type == "FLOAT":
                where_val_converted = float(where_val)
            else:
                where_val_converted = where_val

            # Cascade delete if deleting a Merchant
            if table_name == "Merchants" and where_col == "merchant_id":
                # First delete all transactions for this merchant
                trans_table = self.tables.get("Transactions")
                if trans_table:
                    trans_table.rows = [
                        r for r in trans_table.rows if r[list(trans_table.columns.keys()).index("merchant_id")] != where_val_converted
                    ]

            # Delete rows from the target table
            original_count = len(table.rows)
            table.rows = [r for r in table.rows if r[col_index] != where_val_converted]
            deleted_count = original_count - len(table.rows)

            self.save()

            return f"{deleted_count} row(s) deleted"

        return "Command not recognized by this Database Engine"
