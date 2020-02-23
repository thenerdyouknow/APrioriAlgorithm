import random
import string

final_transactions = []
for i in range(50):
	current_transaction = []
	number_of_items = random.randrange(1,10)
	for j in range(number_of_items):
		random_item = random.randrange(1,20)
		if random_item not in current_transaction:
			current_transaction.append(str(random_item))
	final_transactions.append(current_transaction)

with open('dummy_dataset.txt','w') as open_file:
	for each_transaction in final_transactions:
		for each_item in each_transaction:
			open_file.write(each_item)
			open_file.write(" ")
		open_file.write("\n")