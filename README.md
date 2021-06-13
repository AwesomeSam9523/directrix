# Directrix Bank
![Login Page](https://media.discordapp.net/attachments/853540750616821791/853671281541775410/unknown.png?width=1280&height=720)
## About
This is a GUI bank made using python and connected to SQL. This is a demo about how bank management system works.

## Features
- ### Customers
  - Open & close a bank account
  - Minimum balance to be maintained
  - A way to transfer money to other accounts
  - View their bank statements
  - Take loans on a rate of interest
  - Open a fixed deposit (F.D.)

- ### Bank Staff
  - See daily transactions
  - View transactions of any account
  - View accounts with highest balance maintained

## Approach
The frontend is made using `tkinter` and connected to MySQL database at backend. All user data is saved in bank's database with a similar structure:

Table: `AccountDetails`
AccountID | PersonName | Balance | RegDate |
--------- | ---------- | ------- | ------- |
 | | | |
 
 
Table: `Loans`
AccountID | LoanAmount | StartDate | EndDate | Tenure
--------- | ---------- | --------- | ------- | ------
 | | | | 


Table: `FixedDeposits`
AccountID | Amount | InterestRate | StartDate | Tenure
--------- | ------ | ------------ | --------- | ------
 | | | | 

## System Requirements
- Python 3.8+
- MySQL 8.0+

## Modules used
- Please refer `requirements.txt` for this

## Contributors
1. [Samaksh Gupta](https://github.com/AwesomeSam9523)
2. [Vatsal Saxena](https://github.com/vatsal2025)
