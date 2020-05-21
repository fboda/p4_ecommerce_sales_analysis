#!/usr/bin/env python
# coding: utf-8

# 
# <hr style="height: 4px; color: #839D2D; width: 100%; ">
# 
# # <font color='#61210B'>Formation OpenClassRooms   -   Parcours DATA ANALYST</font>
# 
# <hr style="height: 2px; color: #839D2D; width: 100%; ">
# 
# ## <font color='#38610B'>Projet IV - Analysez les ventes de votre entreprise</font>
# <u>Mise en situation</u>  
# Vous êtes Data Analyst d'une grande chaîne de librairie, fraîchement embauché depuis une semaine !  
# Le service informatique vous a donné l’accès à la base de données des ventes. A vous de vous familiariser avec les données, et de les analyser. Votre manager souhaite que vous réalisiez une présentation pour vous "faire la main".  
# 
# ### Mission 2 - Analyse & Graphes
# 
# - <b>Etude Dataframe Clients</b>
#      - Répartition des Ages par client (Fig.M2.1)
#      - Age des Clients par Tranches (Fig.M2.2)
#      - Répartition des Clients par Sexe (Fig.M2.3)
#      - Les 10 plus gros Clients en terme de CA (Fig.M2.4)
# - <b>Etude Dataframe Produits</b>
#      - Distribution des Tarifs Produits par Catégorie (Fig.M2.5) / Skewness (M25bis)
#      - Les 10 Produits les plus vendus toutes catégories confondues (Fig.M2.6)
#      - Les 10 Produits dont le CA(€) est le plus fort (Fig.M2.6bis)
# - <b>Etude des Transactions</b>
#      - Superposition des analyses suivantes (Fig.M2.7):
#          - Evolution des Ventes Annuelles (courbe/fonction y=f(x)
#          - Nombre de Ventes par Catégorie par Mois (Barchart multiple)
#      - Distribution des CA mensuels sur 1an par catégorie de produits (Fig.M2.8)
#      - Nombre de Ventes de chaque catégorie par Tranches Horaires (Fig.M2.9)
# - <b>Courbe de Lorenz / Indice de Gini</b>
#      - Distribution des Ventes (%) <b>VS</b> (%) Ventes Cumulées sur 1 an (Fig.M2.10)
# 
# 
# **<font color='#38610B'>- Date : 31 Jan 2019</font>**  
# Auteur : Frédéric Boissy
# <hr style="height: 4px; color: #839D2D; width: 100%; ">
# 

# #####   <font color='#013ADF'>ENVIRONNEMENT DE TRAVAIL :</font> Définition - Initialisation

# In[1]:


# -*- coding: utf8 -*-
import numpy as np
import pandas as pd
pd.options.display.float_format = '{:,.2f}'.format   # Nombres avec sepa milliers "," et 2décimales après "."
pd.options.mode.use_inf_as_na = True

import seaborn as sns
import matplotlib as matplt
import matplotlib.pyplot as plt
from matplotlib import patches

import scipy as sc
import scipy.stats as st
import statsmodels as sm

from IPython.display import display, Markdown, HTML  # pour gérer un affichage plus joli que la fonction "print"

import time   # Librairie temps pour calculs durée par exemple
trt_start_time = time.time()


# In[2]:


# Pour executer des requetes SQL de verification sur des DF
from pandasql import sqldf
execsql = lambda q: sqldf(q, globals())   
# req1 = ''' Select zone1, zone2 From DataFrame Where zone3=xx and zone4='xx' limit 3;'''
# df1 = execsql(req1)
# df1


# #####   <font color='#013ADF'>REPERTOIRE DE TRAVAIL :</font> (du Projet)
# Par defaut on utilisera celui dans lequel se trouve ce fichier jupyter

# In[3]:


get_ipython().run_line_magic('cd', 'OUTFILES')


# #####   <font color='#013ADF'>CHARGEMENT DATA "csv" :</font> après nettoyage des donnés dans un Dataframe enrichi

# In[4]:


sal = pd.read_csv("m2_sales_avec_outliers_sans_imput_ref.zip")
sal_ref = pd.read_csv("m2_sales_avec_outliers_avec_imput_ref.zip")
cst = pd.read_csv("cst.csv")
prd = pd.read_csv("prd.csv")
sal.info()
sal_ref.info()


# <hr style="height: 3px; color: #839D2D; width: 100%; ">
# 
# #  <font color='#61210B'><u>Mission n°2</u></font> : Analyse & Graphes
# 

# <hr style="height: 1px; color: #839D2D; width: 100%; ">
# 
# ## <font color='#013ADF'>ETUDE DES CLIENTS
# * Analyse <strong>"simple"</strong> faite à partir des données de la table "client" (Dataframe <strong>"cst"</strong>)

# ### <u><font color='darkred'>Repartition en fonction de l'age</font></u>

# In[5]:


df1 = cst.copy()
fig = plt.figure(figsize=(20,10))

sns.set_style("whitegrid")
ax = sns.countplot(df1['age'], orient="v")
ax.set_xlim(left=-1)
# TITRE GRAPHE 
plt.title("Répartition Age des Clients", fontsize=20, color = 'Blue', y=1.05)
# Libellé Abscisse (x)
plt.xticks(rotation=60, size=13)
plt.xlabel("Age", color="black", size=20)              
# Libellé Ordonnée (y)
plt.yticks(size=15)
plt.ylabel("Nombres", color='black', size=20, rotation=90)      

plt.figtext(0.5,0.02,'(Figure M2.1)', fontsize=12, color = 'gray')
plt.savefig('figure_M21.png', dpi=100, bbox_inches='tight')

plt.show()
plt.close()

#df1.groupby(['age']).size().reset_index(name='counts').head(5)


# ### <u><font color='darkred'>Repartition par Tranches d'age</font></u>

# In[6]:


df2 = cst.copy()
tranches = [0, 19, 39, 59, 75, 100]
nom_tranches = ["0/19","20/39","40/59","60/75", "76+"]
df2['tranches'] = pd.cut(df2.age, tranches, labels = nom_tranches)
df2 = df2.sort_values(['tranches', 'age'])

fig = plt.figure(figsize=(8,6))
ax = sns.countplot(df2['tranches'], palette='cubehelix')
# TITRE GRAPHE 
plt.title("Age des Clients par Tranches", fontsize=20, color = 'Blue', y=1.05)
# Libellé Abscisse (x)
plt.xticks(size=13)
plt.xlabel("Age", color="black", size=20)              
# Libellé Ordonnée (y)
plt.yticks(size=13)
plt.ylabel("Nombres", color='black', size=20, rotation=90)      

plt.figtext(0.45,-0.03,'(Figure M2.2)', fontsize=12, color = 'gray')
plt.savefig('figure_M22.png', dpi=100, bbox_inches='tight')

plt.show()
plt.close()
df2.groupby(['tranches']).size().reset_index(name='counts').head(5)


# ### <u><font color='darkred'>Repartition par Sexe</font></u>

# In[7]:


df3 = cst.groupby(['sex'])['age'].agg(["count"])
H = df3.loc['m']['count']
F = df3.loc['f']['count']

# Pie chart
vals = [H, F]
libelles = ['Hommes', 'Femmes']

fig = plt.figure(figsize=(6,4))
plt.pie(vals, labels=libelles, autopct='%0.1f%%', shadow=True, radius=1.2, 
        explode=[0.1,0], startangle=-110, textprops={'fontsize': 20})
plt.title("Repartition des Clients / Sexe", fontsize=20, color = 'Blue', y=1.05)

plt.figtext(0.2,0.02,'(Figure M2.3)', fontsize=12, color = 'gray')
plt.savefig('figure_M23.png', dpi=100, bbox_inches='tight')

plt.show()
plt.close()
df3.head()


# ### <u><font color='darkred'>Les 10 plus gros Clients en terme ce CA(€) annuel</font></u>

# In[8]:


df4 = sal.groupby(['client'])['price'].sum().reset_index()
df4 = df4.sort_values(['price'], ascending=False).head(10)

# TITRE GRAPHE 
fig = plt.figure(figsize=(10,6))
ax = sns.barplot(x="price", y="client", orient='h', data=df4)
plt.title("Les 10 plus Gros Client en Terme de CA(€) Annuel", fontsize=20, color = 'Blue', y=1.05)
# Libellé Abscisse (x)
plt.xticks(size=13)
plt.xlabel("CA(€) Annuel", color="black", size=20)              
# Libellé Ordonnée (y)
plt.yticks(size=13)
plt.ylabel("Clients", color='black', size=20, rotation=90)      

plt.figtext(0.5, -0.05,'(Figure M2.4)', fontsize=12, color = 'gray')
plt.savefig('figure_M24.png', dpi=100, bbox_inches='tight')

plt.show()
plt.close()
df4


# > Nous constatons qu'il y a 4 très gros clients !!!  Dont les achats sur 1an s'élèvent à plus de 50'000 €  
# Ce ne sont probablement pas des "particuliers" mais plutot des entreprises.  
# <b>Ils seront supprimées pour l'étude des corrélations de la mission 3.<b>

# <hr style="height: 1px; color: #839D2D; width: 100%; ">
# 
# ## <font color='#013ADF'>Etude des Produits (basique)</font>
# 
# * Analyse <strong>"simple"</strong> faite à partir des données de la table "produits" (Dataframe <strong>"prd"</strong>)

# ### <u><font color='darkred'>Distribution des Tarifs Produits / Catégorie</font></u>

# In[9]:


df5 = prd[['categ', 'price']].copy()
df5 = df5.sort_values(['categ', 'price'])
x = df5['categ']
y = df5['price']

sns.set()
fig = plt.figure(figsize=(15,6))
ax = sns.boxplot(y, x, data=df5, orient="h", hue=x, showmeans=True, palette='cubehelix')  ## showfliers=False
ax.set_xlim(right=310)
legend = ax.legend(loc='center right', bbox_to_anchor=(0, 0.5), ncol=1, shadow=True, title='CATEGORIES')
legend.get_title().set_fontsize('15')
plt.setp(plt.gca().get_legend().get_texts(), fontsize='15') #legend 'list' fontsize

# TITRE GRAPHE 
plt.title("Distribution des Tarifs par Catégorie de Produit", fontsize=20, color = 'Blue', y=1.05)
# Libellé Abscisse (x)
plt.xticks(size=15)
plt.xlabel("Prix", color='black', size=20) 
# Libellé Ordonnée (y)
plt.yticks(color="white")
plt.ylabel("")

plt.figtext(0.5, -0.05,'(Figure M2.5)', fontsize=12, color = 'gray')
plt.savefig('figure_M25.png', dpi=100, bbox_inches='tight')

plt.show()
plt.close()


# > * Moyenne > Mediane  :  distribution asymétrique à droite, ou skewness droit

# In[10]:


fig = plt.figure(figsize=(11,5))
sns.set_style("whitegrid")
sns.distplot(df5[df5['categ']==0]['price'] , color="darkgreen")
sns.distplot(df5[df5['categ']==1]['price'] , color="saddlebrown")
sns.distplot(df5[df5['categ']==2]['price'] , color="mediumpurple")

# TITRE GRAPHE 
plt.title("Skewness/Asymétrie Droite Tarifs Produits / Catégorie", fontsize=15, color = 'Blue', y=1.05)
# Libellé Abscisse (x)
plt.xticks(size=12)
plt.xlabel("Prix", color='black', size=15) 
# Libellé Ordonnée (y)
plt.ylabel("Nombre", color='black', size=15) 
plt.yticks(color="white")
plt.figtext(0.11, 0.74,'0        50     100    150     200     250     300', fontsize=12, rotation=90)

plt.figtext(0.47, -0.05,'(Figure M2.5bis)', fontsize=12, color = 'gray')
plt.savefig('figure_M25bis.png', dpi=100, bbox_inches='tight')

plt.show()
plt.close()

df51 = df5[df5['categ']==0].describe(include="all")
df52 = df5[df5['categ']==1].describe(include="all")
df53 = df5[df5['categ']==2].describe(include="all")
df5result = pd.concat([pd.concat([df51, df52], axis=1, join='inner'), df53], axis=1, join='inner')
df5result


# ### <u><font color='darkred'>Les 10 produits les plus vendus (Fig.6) /// Les 10 dont le CA(€) est le plus haut (Fig.6bis)</font></u>

# In[11]:


# GRAPHE 1
df6nbr = sal.groupby(['prod'])['price'].size().reset_index(name='counts').sort_values(['counts'], ascending=False).head(10)

fig = plt.figure(figsize=(8,5))
ax = sns.barplot(x="counts", y="prod", orient='h', data=df6nbr)
plt.title("Les 10 Produits les plus vendus (ttes categ.confondues)", fontsize=20, color = 'Blue', y=1.05)
# Libellé Abscisse (x)
plt.xticks(size=13)
plt.xlabel("Nombre de Ventes Annuelles", color="black", size=20)              
# Libellé Ordonnée (y)
plt.yticks(size=13)
plt.ylabel("Produist", color='black', size=20, rotation=90)      

plt.figtext(0.5, -0.05,'(Figure M2.6)', fontsize=12, color = 'gray')
plt.savefig('figure_M26.png', dpi=100, bbox_inches='tight')
plt.show()

# GRAPHE 2
df6val = sal.groupby(['prod'])['price'].sum().reset_index()
df6val = df6val.sort_values(['price'], ascending=False).head(10)

fig = plt.figure(figsize=(8,5))
ax = sns.barplot(x="price", y="prod", orient='h', data=df6val)
plt.title("Les 10 Meilleurs Produits en terme de CA(€) Annuel", fontsize=20, color = 'Blue', y=1.05)
# Libellé Abscisse (x)
plt.xticks(size=13)
plt.xlabel("CA(€) Annuel", color="black", size=20)              
# Libellé Ordonnée (y)
plt.yticks(size=13)
plt.ylabel("Produits", color='black', size=20, rotation=90)      

plt.figtext(0.5, -0.05,'(Figure M2.6bis)', fontsize=12, color = 'gray')
plt.savefig('figure_M26bis.png', dpi=100, bbox_inches='tight')
plt.show()
plt.close()


# <hr style="height: 1px; color: #839D2D; width: 100%; ">
# 
# ## <font color='#013ADF'>Etude des Ventes
# 
# * Analyse faite à partir des données de la table enrichi dans le notebook précédent "sales" (Dataframe <strong>"sal"</strong>)

# ### <u><font color='darkred'>Evolution des Ventes (C.A. Mensuel) sur 1an  & Nombre de Ventes de chaque Catégorie de Produits / Mois </font></u>

# In[12]:


fig = plt.figure(figsize=(18,8))    
# TITRE GRAPHE 
plt.title("Nb Ventes / Catégorie de Produits / Mois  ----  Evolution CA Mensuel", fontsize=20, color = 'Blue', y=1.05)
#plt.figtext(0.15,0.95,'Nb Ventes / Catégorie de Produits / Mois   ---   ', fontsize=25, ha='left', color = 'Black')
#plt.figtext(0.55,0.95,'Evolution CA Mensuel', fontsize=25, ha='left', color = 'darkred')

# -------------------------------------------
#  GRAPHE 1 - Nombre de Ventes (3 Barres)
# -------------------------------------------
df11 = sal.groupby(['period', 'categ']).size().reset_index(name='counts')
ax11 = sns.barplot(x="period", y="counts", hue="categ", data=df11)
ax11.legend(loc='center right', bbox_to_anchor=(0, 0.94), ncol=1, shadow=True, title="Catégories")

#df11 = pd.pivot_table(sal, values='price', index=['period'], columns=['categ'], aggfunc='count').reset_index()
#ax11 = df11.plot(x="period", rot=30, kind='bar', figsize=(18,8))   #  colormap="viridis", "inferno", "summer", "winter"

ax11.set_xlabel('Periode (Mois)', color='black', size=20) 
plt.xticks(size=15)
# Make the y-axis label, ticks and tick labels match the line color.
ax11.set_ylabel('Nb Ventes', color='black', size=20)
ax11.tick_params('y', colors='black', size=5, labelsize=15)

# -------------------------------------------
#  GRAPHE 2 - Courbe Evolution CA
# -------------------------------------------
df12 = sal.groupby(['period'])['price'].agg(["sum"])
x12 = df12.index
y12 = df12['sum']

ax12 = ax11.twinx()
ax12 = sns.lineplot(x12, y12, data=df12, color='darkred')
plt.plot(x12, y12,'o', color = 'darkred')

ax12.set_ylabel('CA', color='darkred', size=20, rotation=-90)
ax12.tick_params('y', colors='darkred', size=5, labelsize=15)
ax12.grid(False)

plt.figtext(0.5, 0,'(Figure M2.7)', fontsize=12, color = 'gray')
plt.savefig('figure_M27.png', dpi=100, bbox_inches='tight')

plt.show()
plt.close()
df11.head()


# ### <u><font color='purple'>Même etude avec Reference 0_2245 prise en compte</font></u>

# In[13]:


fig = plt.figure(figsize=(18,8))    
# TITRE GRAPHE 
plt.title("Nb Ventes / Catégorie de Produits / Mois  ----  Evolution CA Mensuel", fontsize=20, color = 'Blue', y=1.05)
# -------------------------------------------
#  GRAPHE 1 - Nombre de Ventes (3 Barres)
# -------------------------------------------
df11 = sal_ref.groupby(['period', 'categ']).size().reset_index(name='counts')
ax11 = sns.barplot(x="period", y="counts", hue="categ", data=df11)
ax11.legend(loc='center right', bbox_to_anchor=(0, 0.94), ncol=1, shadow=True, title="Catégories")

ax11.set_xlabel('Periode (Mois)', color='black', size=20) 
plt.xticks(size=15)
# Make the y-axis label, ticks and tick labels match the line color.
ax11.set_ylabel('Nb Ventes', color='black', size=20)
ax11.tick_params('y', colors='black', size=5, labelsize=15)

# -------------------------------------------
#  GRAPHE 2 - Courbe Evolution CA
# -------------------------------------------
df12 = sal_ref.groupby(['period'])['price'].agg(["sum"])
x12 = df12.index
y12 = df12['sum']

ax12 = ax11.twinx()
ax12 = sns.lineplot(x12, y12, data=df12, color='darkred')
plt.plot(x12, y12,'o', color = 'darkred')

ax12.set_ylabel('CA', color='darkred', size=20, rotation=-90)
ax12.tick_params('y', colors='darkred', size=5, labelsize=15)
ax12.grid(False)

plt.figtext(0.5, 0,'(Figure M2.7_avec_ref_0_2245)', fontsize=12, color = 'gray')
plt.savefig('figure_M27_avec_ref_0_2245.png', dpi=100, bbox_inches='tight')

plt.show()
plt.close()
df11.head()


# #### TOTAL  Annuel Nb Ventes / Catégorie

# In[14]:


df11tot = df11.groupby(['categ'])['counts'].sum().reset_index()
df11tot


# ### <u><font color='darkred'>CA Mensuels par Categorie  </font></u>(Scatterplots)

# In[15]:


df81 = sal.groupby(['period', 'categ'])['price'].sum().reset_index()
sns.set()
plt.figure(figsize=(8,7))  
ax = sns.scatterplot(x="price",y="period",hue='categ', size="price", sizes=(50, 250), data=df81)
ax.legend(loc=(1.02,0), fontsize=12, shadow=True)

# TITRE GRAPHE 
plt.title("CA Mensuels / Categorie", fontsize=20, color = 'Blue', y=1.05)
# Libellé Abscisse (x)
plt.xlabel("Prix", color='black', size=15) 
plt.xticks(size=13)
# Libellé Ordonnée (y)
plt.ylabel("Periodes/Mois", color="black", size=15, rotation=90)
plt.yticks(size=13)

plt.figtext(0.45, 0,'(Figure M2.8)', fontsize=12, color = 'gray')
plt.savefig('figure_M28.png', dpi=100, bbox_inches='tight')

plt.show()
plt.close()
df81.head()


# ### <u><font color='purple'>Même etude avec Reference 0_2245 prise en compte</font></u>

# In[16]:


df82 = sal_ref.groupby(['period', 'categ'])['price'].sum().reset_index()
sns.set()
plt.figure(figsize=(8,7))  
ax = sns.scatterplot(x="price",y="period",hue='categ', size="price", sizes=(50, 250), data=df82)
ax.legend(loc=(1.02,0), fontsize=12, shadow=True)

# TITRE GRAPHE 
plt.title("CA Mensuels / Categorie", fontsize=20, color = 'Blue', y=1.05)
# Libellé Abscisse (x)
plt.xlabel("Prix", color='black', size=15) 
plt.xticks(size=13)
# Libellé Ordonnée (y)
plt.ylabel("Periodes/Mois", color="black", size=15, rotation=90)
plt.yticks(size=13)

plt.figtext(0.45, 0,'(Figure M2.8_avec_ref_0_2245)', fontsize=12, color = 'gray')
plt.savefig('figure_M28_avec_ref_0_2245.png', dpi=100, bbox_inches='tight')

plt.show()
plt.close()
df82.head()


# #### TOTAL  CA(€) Annuel / Catégorie

# In[17]:


df81tot = df81.groupby(['categ'])['price'].sum().reset_index()
df81tot


# In[18]:


df82tot = df82.groupby(['categ'])['price'].sum().reset_index()
df82tot


# ### <u><font color='purple'>L'impact de la Reference 0_2245 n'est pas très important sur le CA de la catégorie 0</font></u>
# 
# >Un écart constaté de : <b>1062.96 €</b>    
# Soit <b>0,047(%) </b> du chiffres d'affaire annuel

# ### <u><font color='darkred'>Ventes par Tranches horaire</font></u>

# In[19]:


df9 = sal[['categ', 'time', 'prod', 'price']].copy()
heure = df9['time'].str[0:2:1].astype('int')
minute = df9['time'].str[3:5:1].astype('int')/60
df9['hm'] = heure + minute

tranches = [-1,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
nom_tranches = ["0-1","1-2","2-3","3-4", "4-5", "5-6", "6-7", "7-8", "8-9", "9-10", "10-11", "11-12", "12-13", 
                "13-14", "14-15", "15-16", "16-17", "17-18", "18-19", "19-20", "20-21", "21-22", "22-23", "23-0"]
df9['tranches'] = pd.cut(df9.hm, tranches, labels = nom_tranches)
df9 = df9.groupby(['tranches', 'categ'])['prod'].size().reset_index(name='counts')
df9 = df9.sort_values(['tranches'])

sns.set()
ax = sns.relplot(x="tranches", y="counts", height=5, hue="categ", palette="winter", kind="line", aspect=2.0, data=df9)
# TITRE GRAPHE 
plt.title("Nb Ventes par Tranches Horaire et Catégories", fontsize=20, color = 'Blue', y=1.05)
# Libellé Abscisse (x)
plt.xticks(rotation=45, size=13)
plt.xlabel("Heures", color="black", size=20)              
# Libellé Ordonnée (y)
plt.yticks(size=15)
plt.ylabel("Nb Ventes", color='black', size=20, rotation=90)      

plt.figtext(0.47, -0.1,'(Figure M2.9)', fontsize=12, color = 'gray')
plt.savefig('figure_M29.png', dpi=100, bbox_inches='tight')

plt.show()
plt.close()


# #### Nb Ventes Moyenne / Heure

# In[20]:


df9mh = df9.groupby(['categ'])['counts'].mean().reset_index()
df9mh['moyh'] = df9mh['counts'] / 365
df9mh.head()


# <hr style="height: 1px; color: #839D2D; width: 100%; ">
# 
# ## <font color='#013ADF'>Courbe de Lorenz / Indice de Gini</font>
#     
# <u>Fondements de l'analyse :  </u>
# 
# - Une courbe de Lorenz illustre la répartition d'une variable/donnée dans un echantillon/population de cette donnée.  
#   Plus cette courbe est eloignée de la bissectrice, plus les inégalités sont fortes.  
#     
# - Le coefficient de Gini montre, lui, les inégalités au sein de cet échantillon/population.  
#   Il se calcul en faisant le rapport entre l'aire du triangle formé par la bissectrice sur l'aire de la zone délimitée  
#   par la courbe de Lorenz de la variable/donnée observée.  
#   Plus il est proche de 1, plus la population des données est inégalitaires (répartition des données au sein de...).
# 
# 

# 
# ### <u><font color='darkred'>Analyse des Prix de Ventes sur l'année</font></u>

# In[21]:


sal.head()


# * Chargement des valeurs "price" du datafrane des ventes dans une variable et on la <strong>"TRIE"</strong> par ordre croissant !!!

# In[22]:


df10 = sal[['price']].copy()
ventes = df10.sort_values(['price'], ascending=[True])


# #### Détermination de la courbe de <strong>Lorenz</strong>

# In[23]:


# lorenz = np.cumsum(np.sort(priceachats.head()
lorenz = np.cumsum(ventes) / ventes.sum()
lorenz = np.append([0],lorenz) # La courbe de Lorenz commence à 0

fig, ax = plt.subplots(figsize=[10,10])
# TITRE GRAPHE 
plt.title("Courbe de Lorenz - Prix Ventes / 1an", fontsize=20, color = 'Blue', y=1.05)
# Libellé Abscisse (x)
plt.xticks(size=13)
plt.xlabel("Distribution des Ventes (%)", color="black", size=20)              
# Libellé Ordonnée (y)
plt.yticks(size=13)
plt.ylabel("Cumul Prix Ventes (%)", color='black', size=20, rotation=90)      

## Ligne d'égalité
ax.plot([0,1], [0,1], color='black')
## Courbe de Lorenz
plt.plot(np.linspace(0,1,len(lorenz)),lorenz,drawstyle='steps-post')

# TRACE D'UN RECTANGLE pour Analyse
rect = plt.Rectangle((1, 1), -0.2, -0.45, edgecolor = 'darkred', facecolor = '#FBF2EF',
                      fill = True, linestyle = 'dashed', linewidth = 2, zorder = 1)     #  hatch = '/',
ax.add_artist(rect)
# Analyses
plt.figtext(0.45,0.5,'Indice Gini = 39.2%', fontsize=15, color = 'blue', rotation = 45)
plt.figtext(0.22,0.04,'(20% du Nombre de ventes représentent presque 45% du CA Total des Ventes)', fontsize=15, color = 'darkred')
plt.figtext(0.22,0.01,'La repartition du nb de ventes n''est pas trés égalitaire  (Gini)', fontsize=15, color = 'darkred')

plt.figtext(0.47, -0.05,'(Figure M2.10)', fontsize=12, color = 'gray')
plt.savefig('figure_M210(lorenz).png', dpi=100, bbox_inches='tight')

plt.show()
plt.close()


# #### Calcul du coefficient de <strong>Gini</strong>.
# - Calcul de l'aire sous courbe = aire_ss_courbe   (La dernière valeur ne participe pas à l'aire, d'où "[:-1]")
# - Calcul de la Surface (S) entre aire de la 1ere bissectrice et la courbe de Lorenz
# - Coeff.Gini = 2 * S

# In[24]:


aire_ss_courbe = lorenz[:-1].sum()/len(lorenz) 
S = 0.5 - aire_ss_courbe 
# Gini
gini = round(2*S, 3)
Markdown('{}<strong>{}'.format("Coefficient de Gini : ", gini))


# In[25]:


dureetotale = round(time.time() - trt_start_time, 5)
print("--- Durée TOTALE du Notebook PJ4 Mission 2 --- ", "%s seconds" % dureetotale)

