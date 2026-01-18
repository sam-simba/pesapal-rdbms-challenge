from pesa_rdbms.engine import DatabaseEngine

def start_repl():
    db = DatabaseEngine()
    print("Welcome to Pesapal Mini-RDBMS with tables: 'Merchants' and 'Transactions'. Type 'exit' or press Ctrl + C to quit.")

    while True:
        command = input("> ")
        if command.lower() == "exit":
            break
        result = db.execute(command)
        print(result)

if __name__ == "__main__":
    start_repl()
