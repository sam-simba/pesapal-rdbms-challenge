Please view in Github in code mode

PesaMerchants/
├── app.py . . . . . . . . . . . # Flask web application entry point
├── repl.py . . . . . . . . . . .# Mini-RDBMS REPL and DatabaseEngine
├── tables.py . . . . . . . . . .# Table class: rows, columns, indexing
├── data.json . . . . . . . . . .# Persistent storage of tables and rows (auto-created)
├── templates/ . . . . . . . . . # HTML templates for rendering web pages
│ ├── index.html . . . . . . . . # Homepage showing Merchants & Transactions tables
│ ├── add.html . . . . . . . . . # Form template for adding Merchant or Transaction
│ └── update.html . . . . . . . .# Form template for updating rows
├── static/ . . . . . . . . . . .# CSS styling
│ └── style.css
└── design.md . . . . . . . . . .# project design overview
