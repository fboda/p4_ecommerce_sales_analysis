# -----------------------------------------
#    Nettoyage Données - valeurs nulles
#    Clés Primaires   
# -----------------------------------------

# - CUSTOMERS
Select Count(*) From customers;
Delete From customers Where client_id Is Null;
Select Max(Length(client_id)), Max(Length(sex)), Max(Length(birth))
From customers;

Alter Table customers
Change Column client_id  client_id Varchar(8) Not Null,
Change Column sex        sex       Varchar(1) Not Null,
Add Primary Key (client_id);


# - PRODUCTS
Select Count(*) From products;
Delete From products Where id_prod is null;
Select Max(Length(id_prod)), Max(Length(price)), Max(Length(categ))
From products;

Alter Table products 
Change Column id_prod  id_prod  Varchar(8) Not Null,
Change Column categ    categ    Varchar(1) Not Null,
Add Primary Key (id_prod);


# - TRANSACTIONS
Select count(*) From transactions;
Delete From transactions Where client_id is null;
Delete From transactions Where id_prod is null;
Select Max(Length(client_id)), Max(Length(id_prod)), Max(Length(session_id)), Max(Length(date))
From transactions;

Alter Table transactions
Change Column client_id  client_id    Varchar(8) Not Null,
Change Column id_prod    id_prod      Varchar(8) Not Null,
Change Column session_id session_id   Varchar(8) Not Null,
Change Column date       session_date Varchar(31) Not Null,
Add Column year   Int(5) Not Null After client_id,
Add Column month  Int(2) Not Null After year,
Add Column day    Int(2) Not Null After month;

Alter Table transactions
Add Primary Key (session_id, session_date); 

# Probleme pour definir la clé primaire ==> Erreur sur la zone session date qui n'est pas unique ??!!

# ---------------------------------------------
#      ANALYSE - Valeurs aberrantes
# ---------------------------------------------
#   Suppression diverese & formattage
#   dans les 3 tables
# --------------------------------------
Select Distinct substr(session_date, 1, 4)
From   transactions;

# Products  ---------------------------
Select distinct id_prod
From   transactions
Where  session_date like 'test%';

Delete From products
Where  id_prod like 'T_%';

# Customers ---------------------------
Select distinct client_id
From   transactions
Where  session_date like 'test%';

Delete From customers
Where  client_id like 'ct_%';

# Transactions ------------------------

# Supprimer les lignes de transactions 
# dont les clients et produits n'existent 
# pas dans les tables "products" et "customers"
Select *
From   transactions
Where  session_date like 'test%';

OPTIMIZE TABLE transactions;

Delete    transactions From transactions 
Left Join customers    On (transactions.client_id = customers.client_id) 
Where     customers.client_id Is Null;

Delete    transactions From transactions 
Left Join products    On (transactions.id_prod = products.id_prod) 
Where     products.id_prod Is Null;

Select * From transactions
Where  session_date like 'test%';

# Maintenant on peut définir la clé primaire
Alter Table transactions
Add Primary Key (session_id, session_date); 


# -----------------------------------------------
#   MISE A JOUR nouvelles zones créées
#   CREATION TABLE "VENTES" générale exhaustive
#   pour export et analyse sur Jupyter Notebook
# -----------------------------------------------
Update transactions
Set year    = cast(substr(session_date, 1, 4) as dec(4)),
      month = cast(substr(session_date, 6, 2) as dec(2)),
	  day     = cast(substr(session_date, 9, 2) as dec(2));

Select session_id, session_date, count(*) From Transactions
Group by session_id, session_date
Having count(*) > 1;


CREATE TABLE sales (
  salesdate     varchar(31) NOT NULL,
  session_id    varchar(8)  NOT NULL,
  year          int(4)      NOT NULL,
  month         int(2)      NOT NULL,
  day           int(2)      NOT NULL,
  client_id     varchar(8)  NOT NULL,
  sex           varchar(1)  NOT NULL,
  birth         int(4)      NOT NULL,  
  id_prod       varchar(8)  NOT NULL,
  categ         varchar(1)  NOT NULL,
  price         double      NOT NULL,
  PRIMARY KEY (session_id, salesdate)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

Insert Into Sales
Select 
t.session_date, t.session_id,
t.year, t.month, t.day, 
t.client_id, c.sex, c.birth,
t.id_prod, p.categ, p.price
From transactions t 
Left Join Customers c On t.client_id = c.client_id
Left Join Products p On t.id_prod = p.id_prod;

SELECT * INTO OUTFILE '/result.csv'
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
FROM products;

Select * From sales;
