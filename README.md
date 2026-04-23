# elite102-banking-app
A simple banking app that allows you te create your own account (sign in or log in), allows for money transfers between accounts, and has a transaction history per user.
It was created with mySQL, Python, and Flask. 

IMPORTANT
At this momment, the database only runs locally on my machine. Therefore, if you want to run it, you will have to create your own database, and put a .env with your database info. 
Here is a mySQL query script to replicate my databases:


CREATE DATABASE IF NOT EXISTS banking_app;
USE banking_app;

CREATE TABLE bank_accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    balance DECIMAL(10,2) NOT NULL
);

CREATE TABLE bank_transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    id INT NOT NULL,  
    balance DECIMAL(10,2) NOT NULL,
    date DATETIME NOT NULL,
    FOREIGN KEY (id) REFERENCES bank_accounts(id)
);

