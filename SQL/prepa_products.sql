# --------------------------------------
#      MAJ Colonnes et Clé Primaire
# --------------------------------------
Select Count(*) From products;

Delete From products Where id_prod is null;

Select Max(Length(id_prod)), Max(Length(price)), Max(Length(categ))
From products;

Alter Table `pj4`.`products` 
Change Column `id_prod` `id_prod` VARCHAR(8) NOT NULL ,
Change Column `categ` `categ` VARCHAR(1) NOT NULL,
Add Primary Key (`id_prod`);

# --------------------------------------
#      Nettoyage Données 
# --------------------------------------

# Suppression des lignes dont le prix est négatif
Delete From products Where price <= 0;

Select categ, count(*)
From products
Group by categ;

Select id_prod, count(*)
From products
Group by id_prod
Having count(*) > 1;

Select * From products;
