# Pesapal RDBMS Challenge

This repository contains my solution for the Pesapal Developer '26 Challenge.  
It demonstrates a simple RDBMS with CRUD operations and a trivial web app using Python and Flask.
The database engine allows for simple SQL statements such as **SELECT, INSERT, UPDATE, DELETE and JOIN**. Other operations such as aggregations, GROUP BY, ORDER BY etc. are unavailable.

Please use the Code mode on Github for README.md to visualise the structure correctly.

---

Please check the short video files **docs/app_repl.mp4** and **docs/repl_guide.mp4** for a headstart into running the project (repl.py and app.py)

---

## Features

- **Custom RDBMS**
  - Tables: `Merchants` and `Transactions`
  - Supported data types: `INT`, `FLOAT`, `TEXT`
  - CRUD operations: `CREATE`, `READ`, `UPDATE`, `DELETE`
  - Basic query interface via REPL
    - python repl.py

- **Sample Data**
  - Merchants: Sami Wachira, Lucy Maimuna, John Otieno
  - Transactions with various payment methods (Mpesa, Equity Card, KCB Card, NCBA Card) - Please check the SQL insert, update, and delete codes below for reference

- **Flask Demo**
  - Simple web app demonstrating CRUD operations
    - python app.py

---

## Requirements

- Python 3.10+
- Flask
- (Optional) Virtual environment for package isolation and seamless running of the web app via python app.py

**Install dependencies:**

````bash
pip install -r requirements.txt

## How to Test
### REPL
python repl.py

### Web Demo
``` bash
python app.py


**Constraints**
1. Primary keys autoincrement and remains unique
2. Emails must be unique.
3. Transactions can only post if the the merchant with the merchant_id exists.
4. Database engine configuration: Deleting a merchant deletes all corresponding transactions.
5. Only "SELECT *" statement function available for this project.


**Getting Started**
-- Please copy the insert statements in one go and paste them in REPL
****************************************
INSERT INTO Merchants VALUES ("Sami Wachira", "s_wachira@pesapal.com");
INSERT INTO Merchants VALUES ("Lucy Maimuna", "l_maimuna@pesapal.com");
INSERT INTO Merchants VALUES ("John Otieno", "j_otieno@pesapal.com");


INSERT INTO Transactions VALUES (2, 1200, "M-Pesa");
INSERT INTO Transactions VALUES (3, 5000, "M-Pesa");
INSERT INTO Transactions VALUES (1, 75000, "M-Pesa");
INSERT INTO Transactions VALUES (1, 15000, "Equity Card");
INSERT INTO Transactions VALUES (2, 90000, "Equity Card");
INSERT INTO Transactions VALUES (3, 45000, "KCB Card");
INSERT INTO Transactions VALUES (3, 220000, "KCB Card");
INSERT INTO Transactions VALUES (2, 130000, "NCBA Card");


-- View all records
****************************************
SELECT * FROM Merchants;
SELECT * FROM Transactions;

-- Indexing
****************************************
CREATE INDEX id_merchants ON Transactions (merchant_id)

-- JOIN
****************************************
SELECT * FROM Merchants LEFT JOIN Transactions ON Merchants.merchant_id = Transactions.merchant_id


--Update a record from each table
***************************************
UPDATE Merchants SET email="sami.wac@pesapal.com" WHERE merchant_id=1;
UPDATE Transactions SET amount=899999 WHERE transaction_id=3;


-- Run code to see changes
****************************************
SELECT * FROM Merchants;
SELECT * FROM Transactions;


-- Delete record in Transactions table
****************************************
-- Delete the transaction
DELETE FROM Transactions WHERE transaction_id=8;

-- Show all remaining transactions
SELECT * FROM Transactions;


-- Delete record in Merchants and all related transactions in Transactions table
****************************************
-- Delete all transactions for merchant_id = 2
DELETE FROM Transactions WHERE merchant_id=2;

-- Delete the merchant
DELETE FROM Merchants WHERE merchant_id=2;
As per the db egine configuration's, this code deletes both the merchant and corresponding transactions
````
