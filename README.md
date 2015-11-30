COMS6111 P3 Extract Association Rules

a. Team members:
Jiayi Yan  - jy2677
Jiaying Xu - jx2238

b. Files:
README
apriori.py
main.py

c. How to run
python main.py <filename> <min_supp> <min_conf>
<account key>: 	csv file name
<t_es>:   		float in (0, 1)
<t_ec>:       	float in (0, 1)




Part 2 Association Rule Mining Algorithm
1. Read and parse the input csv file, and generate large 1-itemsets at the same time.
Large word sets and their locations in the document are recorded.
2. Generate k-itemsets using k-1-itemsets .
3. Remove itemsets whose subsets are not in k-1-itemsets.
   Calculate support and remove itemsets with support less than min_supp
   Calculate confidence
4. Repeat step 2,3 until no more item sets can be generated.

