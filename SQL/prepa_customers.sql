# --------------------------------------
#      MAJ Colonnes et Clé Primaire
# --------------------------------------
Select Count(*) From customers;

Delete From customers Where client_id is null;

Select Max(Length(client_id)), Max(Length(sex)), Max(Length(birth))
From customers;

Alter Table `pj4`.`customers` 
Change Column `client_id` `client_id` VARCHAR(8) NOT NULL ,
Change Column `sex` `sex` VARCHAR(1) NOT NULL,
Add Primary Key (`client_id`);

# --------------------------------------
#      Nettoyage Données 
# --------------------------------------

Select Substr(client_id, 1, 2) as part, count(*)
From customers
Group by part;

Select client_id, count(*)
From customers
Group by client_id
Having count(*) > 1;

Select * From customers;

