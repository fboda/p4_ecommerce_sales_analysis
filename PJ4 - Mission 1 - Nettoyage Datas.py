#!/usr/bin/env python
# coding: utf-8

# <hr style="height: 4px; color: #839D2D; width: 100%; ">
# 
# # <font color='#61210B'>Formation OpenClassRooms   -   Parcours DATA ANALYST</font>
# 
# <hr style="height: 2px; color: #839D2D; width: 100%; ">
# 
# ## <font color='#38610B'>Projet IV - Analysez les ventes de votre entreprise</font>
# 
# ### Mission 1 - Nettoyage des données
# Données extraites directement de la base de l’entreprise vers les fichiers CSV (<a href="https://s3-eu-west-1.amazonaws.com/static.oc-static.com/prod/courses/files/parcours-data-analyst/dataset_P4.zip">Lien</a>)  
# Voici les DataFrames pandas contenant ces tables/fichiers :  
# * <font color='#8A0808'>DataFrame <strong>cst</strong></font> : Table "customers.csv" (liste des clients)
# * <font color='#8A0808'>DataFrame <strong>prd</strong></font> : Table "products.csv" (liste des produits)
# * <font color='#8A0808'>DataFrame <strong>tra</strong></font> : Table "transactions.csv" (historique des ventes)  
#  
#   
# * <font color='#013ADF'>DataFrame <strong>sal</strong></font> : Fichier enrichi pour analyses des ventes
# 
# **<font color='#38610B'>- Date : 31 Jan 2019</font>**  
# Auteur : Frédéric Boissy
# <hr style="height: 4px; color: #839D2D; width: 100%; ">
# 

# #####   <font color='#013ADF'>ENVIRONNEMENT DE TRAVAIL :</font> Définition - Initialisation

# In[ ]:


# -*- coding: utf8 -*-
import numpy as np
import pandas as pd
pd.options.display.float_format = '{:,.2f}'.format   # Nombres avec sepa milliers "," et 2décimales après "."
pd.options.mode.use_inf_as_na = True

import seaborn as sns
import matplotlib as matplt
import matplotlib.pyplot as plt
import scipy as sc
import scipy.stats as scst
import statsmodels as st

from IPython.display import display, Markdown, HTML  # pour gérer un affichage plus joli que la fonction "print"

import time   # Librairie temps pour calculs durée par exemple
trt_start_time = time.time()


# #####   <font color='#013ADF'>REPERTOIRE DE TRAVAIL :</font> (du Projet)
# Par defaut on utilisera celui dans lequel se trouve ce fichier jupyter - Puis on spécifie le dossier DATA

# In[ ]:


get_ipython().run_line_magic('cd', 'DATA')


# #####   <font color='#013ADF'>CHARGEMENT DES TABLES "csv" :</font> dans les Dataframes "Pandas"

# In[ ]:


cst = pd.read_csv("customers.csv")
prd = pd.read_csv("products.csv")
tra = pd.read_csv("transactions.zip", sep=";")


# <hr style="height: 3px; color: #839D2D; width: 100%; ">
# 
# ###  <font color='#61210B'><u>Table Client</u></font> : Dataframe 'cst'
# - Choix Clé Primaire : <strong>'client_id'</strong>

# In[ ]:


cst.head()


# * **Recherche de Valeurs Nulles** et suppression sur la clé primaire et init des autres colonnes

# In[ ]:


cst.dropna(subset=['client_id'], inplace=True)
cst.sex = cst.sex.fillna('')
cst.birth = cst.birth.fillna(0)


# In[ ]:


cst.isnull().values.any()


# * **Recherche de Doublons**

# In[ ]:


cst[cst.duplicated(subset=['client_id']) == True].head()
#cst.drop_duplicates(subset='client_id', inplace=True)


# * **Recherche de valeurs aberrantes residuelles**

# In[ ]:


# Valeurs distinctes de la colonne "sex"
cst.sex.unique()


# In[ ]:


cst['age'] = (2022 - cst['birth']).astype('int')


# In[ ]:


cst.info()
cst.describe(include="all")


# <hr style="height: 3px; color: #839D2D; width: 100%; ">
# 
# ###  <font color='#61210B'><u>Table Produits</u></font> : Dataframe 'prd'
# - Choix Clé Primaire : <strong>'categ' / 'id_prod'</strong>

# In[ ]:


prd.head()


# * **Recherche de Valeurs Nulles** et suppression sur la clé primaire et init des autres colonnes

# In[ ]:


prd.dropna(subset=['categ', 'id_prod'], inplace=True)
prd.price = prd.price.fillna(0)
prd.categ = prd.categ.fillna(0)


# In[ ]:


prd.isnull().values.any()


# * **Recherche de Doublons**

# In[ ]:


prd[prd.duplicated(subset=['categ', 'id_prod']) == True].head()
# prd.drop_duplicates(subset=['categ', 'id_prod'], inplace=True)


# * **Recherche de valeurs aberrantes residuelles**

# In[ ]:


# Valeurs distinctes de la colonne "categorie" et leurs quantité respectives
prd.groupby('categ')['id_prod'].count().reset_index()


# In[ ]:


# Recherche de produits ayant un prix négatif
prd[prd.price < 0].head()


# In[ ]:


# Suppression des lignes dont le Produit a un prix négatif
prd.drop(prd[prd.price < 0].index, inplace=True)


# In[ ]:


prd.info()
prd.describe(include="all")


# <hr style="height: 3px; color: #839D2D; width: 100%; ">
# 
# ###  <font color='#61210B'><u>Table Transactions</u></font> : Dataframe 'tra'
# - Choix Clé Primaire : <strong>'session_id' / 'date'</strong>

# In[ ]:


tra.head()


# * **Recherche de Valeurs Nulles** et suppression sur la clé primaire et init des autres colonnes

# In[ ]:


tra.dropna(subset=['session_id', 'date'], inplace=True)
tra.id_prod = tra.id_prod.fillna('')
tra.client_id = tra.client_id.fillna(0)
tra.isnull().values.any()


# * **Recherche de Doublons**

# In[ ]:


tra[tra.duplicated(subset=['session_id', 'date']) == True].head()


# In[ ]:


tra[tra.date.str.contains("test_")].head()


# In[ ]:


# Suppression des valeurs date contentant "test_"
tra.drop(tra[tra.date.str.contains("test_") == True].index, inplace=True)


# ####  <font color='purple'>Traitement de la Reference (0_2245) inexistante dans la table Products</font>  
# 
# ![Data_cleaning_ref_2245.png](attachment:Data_cleaning_ref_2245.png)
# 

# ####  <font color='purple'>Imputation d'une valeur "moyenne" pour la Ref "0_2245" </font>  
# <font color='purple'>On crée une ligne dans la table "products" afin que les ventes correspondantes ne soient pas rejetées à l'opération "merge" suivante.</font>  
# Imputation de la valeur <b>"médiane"</b> du prix de la catégorie  (peut différent de la moyenne : 10.32 vs 11.73)

# In[ ]:


prd[prd['categ']==0]['price'].describe()


# In[ ]:


prd = prd.append({'id_prod':'0_2245', 'price':10.32, 'categ':0}, ignore_index=True)
prd.tail()


# <strong>Recherche de valeurs aberrantes residuelles</strong>
# - On ne conserve que les lignes dont les clients existent dans le dataframe "client" : <strong>cst</strong>  
# - On ne conserve que les lignes dont les produits existent dans le dataframe "produits" : <strong>prd</strong>  
# - On supprimer toutes lignes ayant des valeurs "NaN"

# In[ ]:


tra = pd.merge(tra, cst, how='outer')
tra = pd.merge(tra, prd, how='outer')
tra = tra.dropna()


# In[ ]:


tra.isnull().values.any()


# In[ ]:


tra.info()
tra.describe(include="all")


# <hr style="height: 3px; color: #839D2D; width: 100%; ">
# 
# ###  <font color='#61210B'><u>Creation Dataframe "enrichi" des Ventes</u></font> : Dataframe 'sal'
# Ce dataframe contient :  
# * les données de la table/dataframe transactions
# * les données de la table/dataframe clients (+ nelle colonne "age")
# * les données de la table/dataframe produits

# In[ ]:


salm2 = tra.copy()
salm2.columns = ['prod', 'session_date', 'session_id', 'client', 'sex', 'birthyear', 'age', 'price', 'categ']
salm2['age'] = (2022 - salm2['birthyear']).astype('int')
salm2['birthyear'] = salm2['birthyear'].astype('int')
salm2['categ'] = salm2['categ'].astype('int')
salm2['period'] = salm2['session_date'].str[0:7:1]
salm2['year'] = salm2['session_date'].str[0:4:1].astype('int')
salm2['month'] = salm2['session_date'].str[5:7:1].astype('int')
salm2['day'] = salm2['session_date'].str[8:10:1].astype('int')
salm2['time'] = salm2['session_date'].str[11:16:1]

cols = ['session_id', 'client', 'sex', 'age', 'birthyear', 'prod', 'price', 'categ', 'period', 
        'year', 'month', 'day', 'time', 'session_date']
salm2 = salm2[cols]


# In[ ]:


salm2.head()


# <strong>Repérage Données manquantes entre le 1er et le 28 octobre pour la (catégorie 1) </strong>
# 

# In[ ]:


df = salm2.groupby(['period', 'categ'])['prod'].count().reset_index(name="counts")
df = df[df['categ']==1].sort_values(['categ', 'period'])
df


# In[ ]:


df = salm2.groupby(['year', 'month', 'day', 'categ'])['prod'].count().reset_index(name="counts")
df = df[(df['categ']==1)&(df['month']==10)].sort_values(['categ', 'year', 'month', 'day'])
df.head()


# In[ ]:


salm2.info()
salm2.describe(include="all")


# <hr style="height: 3px; color: #839D2D; width: 100%; ">
# 
# ##  <font color='purple'>/// OUTLIERS "Gros Clients", "Age=18ans" & Reference sans prix  ///</font>  
# > <font color='purple'>ACTIONS A MENER AFIN DE NE PAS FAUSSER LES RESULTATS</font>

# #### Lors de la mission 2 et etudes des graphes plusieurs particularités ont été detectées sur ce jeu de données :  
# - Nb elevé de clients pour <B>age = 18ans</B>.  Il s'agit certainement d'une tranche d'age [0-18ans].  
#     > Etude Mission 2 <span style="font-family:Wingdings">&#216;</span> 
#     <b><span style="font-family:Wingdings">&#254;</span> Conservation</b> / 
#     <span style="font-family:Wingdings">&#111;</span>Suppression  
#     > Etude Mission 3 <span style="font-family:Wingdings">&#216;</span> 
#     <span style="font-family:Wingdings">&#111;</span> Conservation / 
#     <b><span style="font-family:Wingdings">&#254;</span>Suppression </b> 
# 
# 
# - <b>4 "Gros cLients"</b> sont à noter. Ce ne sont pas certainement des particuliers : <b>Achats > 50'000 € / An  !!!</b>  
#     > Etude Mission 2 <span style="font-family:Wingdings">&#216;</span> 
#     <b><span style="font-family:Wingdings">&#254;</span> Conservation</b> / 
#     <span style="font-family:Wingdings">&#111;</span>Suppression  
#     > Etude Mission 3 <span style="font-family:Wingdings">&#216;</span> 
#     <span style="font-family:Wingdings">&#111;</span> Conservation / 
#     <b><span style="font-family:Wingdings">&#254;</span>Suppression </b> 
# 
# 
# - Une reference présente <b>(_2245)</b> dans les "ventes", mais sa fiche produit <b>n'existe pas(plus)</b> dans la table products.  
#     > Etude Mission 2 <span style="font-family:Wingdings">&#216;</span> 
#     <b><span style="font-family:Wingdings">&#254;</span> Conservation </b> (comparaison <b>avec/sans</b> imputation valeur moyenne catégorie) / <span style="font-family:Wingdings">&#111;</span>Suppression   
#     > Etude Mission 3 <span style="font-family:Wingdings">&#216;</span> 
#     <b><span style="font-family:Wingdings">&#254;</span> Conservation </b> (<b>avec</b> imputation valeur moyenne catégorie) / <span style="font-family:Wingdings">&#111;</span>Suppression

# ####  <font color='purple'>Suppression des lignes de Ventes des clients "Age=18ans"  (Mission3) </font>  

# In[ ]:


# Suppression des lignes des clients agés de 18ans
salm3 = salm2.copy()
salm3.drop(salm3[salm3.age == 18].index, inplace=True)
salm3.head()


# ####  <font color='purple'>Suppression des lignes de Ventes des 4 Gros clients </font>  

# In[ ]:


# Stocker les 4 plus clients en terme de CA dans une variable tableau
salm3cli = salm3.groupby(['client'])['price'].sum().reset_index()
salm3cli = salm3cli.sort_values(['price'], ascending=False).head(4)
clidel = salm3cli['client'].values
salm3[salm3['client'].isin(clidel)].head()


# In[ ]:


# Suppression des lignes des clients agés de 18ans
salm3.drop(salm3[salm3.client.isin(clidel)].index, inplace=True)


# In[ ]:


salm3.info()
salm3.describe(include="all")


# ####  <font color='purple'>Suppression des lignes de la ref '0_2245' pour comparaison dans mission 2</font>  

# In[ ]:


salm2s = salm2.copy()
salm2s.drop(salm2s[salm2s['prod'] == '0_2245'].index, inplace=True)
salm2s.info()


# <hr style="height: 3px; color: #839D2D; width: 100%; ">
# 
# ###   <font color='#013ADF'>EXPORT des Dataframes consolidés :</font> dans des fichiers "csv"

# In[ ]:


get_ipython().run_line_magic('cd', '..')
get_ipython().run_line_magic('cd', 'OUTFILES')


# In[ ]:


salm2.to_csv('m2_sales_avec_outliers_avec_imput_ref.zip', sep=',', encoding='utf-8', index=False, compression='zip')
salm2s.to_csv('m2_sales_avec_outliers_sans_imput_ref.zip', sep=',', encoding='utf-8', index=False, compression='zip')
salm3.to_csv('m3_sales_sans_outliers_avec_imput_ref.zip', sep=',', encoding='utf-8', index=False, compression='zip')
cst.to_csv('cst.csv', sep=',', encoding='utf-8', index=False)
prd.to_csv('prd.csv', sep=',', encoding='utf-8', index=False)


# In[ ]:


dureetotale = round(time.time() - trt_start_time, 5)
print("--- Durée TOTALE du Notebook PJ4 Mission 1 --- ", "%s seconds" % dureetotale)

