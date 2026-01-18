class Table:
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns 
        self.rows = []
        self.indexes = {}

    def insert(self, values):
        if len(values) != len(self.columns):
            return f"Error: Expected {len(self.columns)} values, got {len(values)}"
        self.rows.append(values)

        # Automatically update all indexes
        for col, idx in self.indexes.items():
            col_idx = list(self.columns.keys()).index(col)
            idx[values[col_idx]] = len(self.rows) - 1

        return "Row inserted successfully"


    def select_all(self):
        return [
            {col: value for col, value in zip(self.columns.keys(), row)}
            for row in self.rows
        ]

    def create_index(self, column_name):
        if column_name not in self.columns:
            return f"Column {column_name} does not exist"
        self.indexes[column_name] = {}
        index_dict = {}
        col_idx = list(self.columns.keys()).index(column_name)
        for row_idx, row in enumerate(self.rows):
            key = row[col_idx]
            index_dict.setdefault(key, []).append(row_idx)
        
        self.indexes[column_name] = index_dict 
        print(f"Index on '{column_name}' created successfully.")
        print("Index dictionary shown below. \n")
        return index_dict
    
    def to_dict(self):
        return {
            "columns": self.columns,
            "rows": self.rows,
            "indexes": self.indexes
        }

    @classmethod
    def from_dict(cls, name, data):
        table = cls(name, data["columns"])
        table.rows = data.get("rows", [])
        table.indexes = data.get("indexes", {})
        return table