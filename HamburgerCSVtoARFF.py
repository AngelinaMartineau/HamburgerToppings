'''
	This file is used to conver the csv file for the hamburgers
	into an ARFF file. 

	The current csv file has two values per row. One value is the 
	time the survey was completed, and the second is a list of the 
	ingredients that were chosen in that response, where each ingredient 
	is separated by a comma and a space. 
'''

import csv 

#This order is important!! It is the order the binary data will
#be stored in.
total_list_of_ingredients = ['Cheese', 'Lettuce', 'Tomato', 
'Pickles', 'Onions', 'Avacado', 'Bacon', 'Mushrooms', 'Eggs', 
'Chill', 'Chopped Chillies', 'Jalapenos', 'Ketchup', 'Mustard', 
'Ranch', 'Mayo', 'Relish', 'Honey Mustard', 'BBQ Sauce', 
'Hot Sauce', 'Thousand island dressing', 'Aioli', 'Chipotle sauce', 
'Honey truffles', 'Potato chips', 'Spicy mustard', 'A1 Sauce']

#Read in the data.
csv_file = open('Hamburger.csv')
csv_reader = csv.reader(csv_file, delimiter=",")
binary_data = []
index = 0
start_date = None
end_date = None

#Modify the data into binary data
for row in csv_reader:
	if index == 1: 
		start_date = row[0]
	if index == 243: 
		end_date = row[0]
	if index != 0:
		#row[0] is the time of the survey response
		#row[1] is the list of ingredients in the survey response. 	
		list_of_ingredients = row[1].strip().split(", ")
		list_of_bits = []

		for item in total_list_of_ingredients: 
			if item in list_of_ingredients:
				list_of_bits.append(1)
				list_of_ingredients.remove(item)
			else: 
				list_of_bits.append(0)
		
		#Print the data that was excluded
		if list_of_ingredients != []:
			print("ROW", index, ": ", list_of_ingredients)
		binary_data.append(list_of_bits)
	
	index += 1

#Write the binary to a new file.
f = open("Hamburger.arff", "w")

#Metadata section
f.write("% 1. Title: Hamburger Toppings Data\n%\n")
f.write("% 2. Sources: \n")
f.write("%\t(a) Survery link: https://forms.gle/THXTrF8uoXpWk6Ad8\n")
f.write("%\t(b) Google Survey's was used for data collection.\n%\n")
f.write("% 3. Information about the survey\n")
f.write("%\t(a) The survey will continue to remain live. Data\n")
f.write("%\t    can be added at any time.\n")
f.write("%\t(b) Survey responses occured from {} to {}.\n".format(start_date, end_date))
f.write("%\t(c) The survey had a list of ingredients and an \'other\'\n")
f.write("%\t    option for ingredients that were not listed.\n%\n")
f.write("% 4. Cleaning done in the python file\n")
f.write("%\t(a) Cleaning done in the python file removes ingredients\n")
f.write("%\t    that were either not actual ingredients or repeats of\n")
f.write("%\t    other ingredients, including:\n")
f.write("%\t\t(i) Extra of an ingredient\n")
f.write("%\t\t(ii) Mention of burger patty (The survey said the\n")
f.write("%\t\t     burger would start with a patty on a bun)\n")
f.write("%\t\t(iii) Personal notes, such as \'This is {name}'s burger.\'\n\n")


#Relation section
f.write("@RELATION Hamburger\n\n")

#Attribute section
for attribute in total_list_of_ingredients: 
	f.write("@ATTRIBUTE \'" + attribute + "\' BINARY\n")

#Data Section
f.write("\n@DATA\n")
for line in binary_data:
	for index in range(len(line)): 
		if index != len(line)-1:
			f.write(str(line[index])+",")
		else: 
			f.write(str(line[index]))
	f.write("\n")
