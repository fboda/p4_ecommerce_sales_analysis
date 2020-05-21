Select max(birth), min(birth) From customers;

Select   birth, count(*) From customers
Group By birth 
Order By birth;

Select   sex, count(*) From customers
Group By sex 
Order By sex;

Select   birth, sex, count(*) From customers
Group By birth, sex 
Order By birth, sex;
