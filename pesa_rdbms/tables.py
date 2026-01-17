class Table:
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns 
        self.rows = []

    def insert(self, values):
        if len(values) != len(self.columns):
            return f"Error: Expected {len(self.columns)} values, got {len(values)}"
        self.rows.append(values)
        return "Row inserted successfully"


    def select_all(self):
        return [
            {col: value for col, value in zip(self.columns.keys(), row)}
            for row in self.rows
        ]
