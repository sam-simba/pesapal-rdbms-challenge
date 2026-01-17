from engine import DatabaseEngine

db = DatabaseEngine()
print("Welcome to Pesapal Mini-RDBMS. Type EXIT to quit.")

while True:
    command = input("> ")
    if command.lower() == "exit":
        break
    result = db.execute(command)
    print(result)
