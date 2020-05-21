# -----------------------------------------
#      Nettoyage Données - valeurs nulles
# -----------------------------------------

Select count(*) From transactions;

Delete From transactions Where client_id is null;

Delete From transactions Where id_prod is null;

Select Max(Length(client_id)), Max(Length(id_prod)), Max(Length(session_id)), Max(Length(date))
From transactions;

# --------------------------------------
#   MAJ Colonnes & Création Nelle zones :
#   - année, mois, jour et alimentation
# --------------------------------------

Alter Table `pj4`.`transactions` 
Change Column `client_id` `client_id` VARCHAR(8) NOT NULL ,
Change Column `id_prod` `id_prod` VARCHAR(8) NOT NULL ,
Change Column `session_id` `session_id` VARCHAR(8) NOT NULL,
Change Column `date` `session_date` VARCHAR(31) NOT NULL,
Add Column `year` INT(5) NOT NULL AFTER `client_id`,
Add Column `month` INT(2) NOT NULL AFTER `year`,
Add Column `day` INT(2) NOT NULL AFTER `month`;

Select Distinct substr(session_date, 1, 4)
From   transactions;

Select *
From   transactions
Where  session_date like 'test%';

Select distinct id_prod
From   transactions
Where  session_date like 'test%';

Select distinct client_id
From   transactions
Where  session_date like 'test%';

# --------------------------------------
#   Suppression des clients & produits 
#   concernés, dans les 3 tables
# --------------------------------------
# Supprimer les lignes de transactions dont les clients et produits n'existent pas dans les tables "products" et "customers"
OPTIMIZE TABLE transactions;

# Customers
Delete From customers
Where  client_id like 'ct_%';

# Products
Delete From products
Where  id_prod like 'T_%';

# Transactions
Delete    transactions From transactions 
Left Join customers    On (transactions.client_id = customers.client_id) 
Where     customers.client_id Is Null;

Delete    transactions From transactions 
Left Join products    On (transactions.id_prod = products.id_prod) 
Where     products.id_prod Is Null;


Delete From transactions
Where  session_date like 'test%';


Update transactions
Set year    = cast(substr(session_date, 1, 4) as dec(4)),
      month = cast(substr(session_date, 6, 2) as dec(2)),
	  day     = cast(substr(session_date, 9, 2) as dec(2))
;







Select session_id, date, count(*) From Transactions
Group by session_id, date
Having count(*) > 1;

# Modification colonnes et clé primaire
Alter Table `pj4`.`transactions` 
Add Primary Key (`session_id`, `session_date`); 



Select * From transactions;
