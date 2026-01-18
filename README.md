# Pesapal RDBMS Challenge

This repository contains my solution for the Pesapal Developer '26 Challenge.  
It demonstrates a simple RDBMS with CRUD operations and a trivial web app using Python and Flask.
The database engine allows for simple SQL statements such as SELECT, INSERT, UPDATE, AND DELETE. Other operations such as aggregations, GROUP BY, ORDER BY etc. are unavailable. 

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
- (Optional) Virtual environment for package isolation

Install dependencies:

```bash
pip install -r requirements.txt




**Getting Started**
-- Adding Records - keys autoincrement, emails must be unique, and transactions can only POST if the merchant with the merchant_id exists. 
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
UPDATE Merchants SET email="sami.wachira@pesapal.com" WHERE merchant_id=1;
UPDATE Transactions SET amount=899999 WHERE transaction_id=3;


-- Run code to see changes
****************************************
SELECT * FROM Merchants;
SELECT * FROM Transactions;


-- Delete record in Transactions table
****************************************
-- Count before deleting
SELECT COUNT(*) AS Total_Transactions FROM Transactions;

-- Delete the transaction
DELETE FROM Transactions WHERE transaction_id=8;

-- Count after deleting
SELECT COUNT(*) AS New_Total_Transactions FROM Transactions;

-- Show all remaining transactions
SELECT * FROM Transactions;


-- Delete record in Merchants and all related transactions in Transactions table
****************************************
-- Delete all transactions for merchant_id = 2
DELETE FROM Transactions WHERE merchant_id=2;

-- Delete the merchant
DELETE FROM Merchants WHERE merchant_id=2;

