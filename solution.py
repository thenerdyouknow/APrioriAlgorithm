import re
import sys
import itertools
import copy
from collections import Counter

DATASET_FILE = 'dummy_dataset.txt'

#reading all the transactions from the file
with open(DATASET_FILE,'r') as open_file:
	file_contents = open_file.readlines()

#data cleaning process
all_transactions = []
#looping through each line in the file, which is a transaction
for each_transaction in file_contents:
	#removing the \n from each string
	cleaned_string = re.sub('\n','',each_transaction).strip()
	#split the string on spaces, thus getting the items
	split_string = cleaned_string.split(" ")
	#converting string numbers to int numbers
	# int_string = tuple([int(x) for x in split_string])
	int_string = tuple(split_string)
	#appending cleaned transaction to a list containing all the transactions
	all_transactions.append(int_string)

def flatten_list(list_to_flatten):
	#loops through outer list and then inner listen to flatten a list of lists or tuples.
	flat_list = []
	for sublist in list_to_flatten:
		for item in sublist:
			flat_list.append(item)
	return flat_list

def prune(counter_dict,support):
	# removes any key for which the frequency is less than the support value
	pruned_dict = {}
	for key,value in counter_dict.items():
		if(value>=support):
			pruned_dict[key] = value
	return pruned_dict

def generate_frequencies(transactions,item_sets):
	#checks each transaction to see if any of the itemsets are a subset of the transaction. if so, adds one to the count of that itemset.
	counter_dict = {}
	for each_transaction in transactions:
		for each_itemset in item_sets:
			#checks if itemset is subset of transation
			if(set(each_itemset).issubset(each_transaction)):
				try:
					counter_dict[each_itemset] += 1
				except KeyError:
					#if KeyError happens it means the current itemset doesn't exist in the dict yet, so we add it.
					counter_dict[each_itemset] = 1
	return counter_dict

def generate_itemsets(item_sets,combination_size):
	#generates new itemsets given previous itemsets and size of the newer itemset
	new_itemsets = []
	items_to_match = combination_size - 2
	for each_itemset in item_sets:
		#removes the current item from the itemset
		rest_of_itemsets = [item_set for item_set in item_sets if item_set!=each_itemset]
		for every_itemset in rest_of_itemsets:
			#checks if the beginning k-2 items are the same, if yes then it can be merged to form a bigger itemset
			if(every_itemset[:items_to_match+1] == each_itemset[:items_to_match+1]):
				combined_itemset = tuple(sorted(set(every_itemset+each_itemset)))
				new_itemsets.append(combined_itemset)
	#removes duplicates by doing set
	return list(set(new_itemsets))


support = 500
all_combinations = []
i = 1

while True:

	if(i==1):
		#for the first one, flattening the list and just running Counter works fine to get frequencies of each item
		flattened_list = flatten_list(all_transactions)
		counter_dict = Counter(flattened_list)
	else:
		counter_dict = generate_frequencies(all_transactions,all_combinations)

	pruned_dict = prune(counter_dict,support)

	if(i==1):
		#for the first iteration, we can use itertools.combinations to give us set of all combinations
		all_combinations = list(itertools.combinations(sorted(list(pruned_dict)),2))
	else:
		all_combinations = generate_itemsets(list(pruned_dict),i)

	#if there are no combinations in all_combinations then there are no more frequent itemsets, so we can quit
	if not(bool(all_combinations)):
		print("Can't generate any more itemsets, process ends here!")
		sys.exit(0)
		
	i+=1 

