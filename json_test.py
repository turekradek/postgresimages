import json
import uuid
import random
from datetime import datetime, timedelta

# Create a list to store the data
data = []

def check_letters(word):
    small = [ chr(i) for i in range( 97,123)]
    big = [ chr(i) for i in range( 65,98)]
    for letter in word:
        if letter not in small or letter not in big:
            return False
    return True


lista1 = []
def imiona( file_name ):
    with open(f'{file_name}.txt','r') as imiona:
        for el in imiona:
            linia = imiona.readline()
            linia = linia.split()
            print( linia, end='' )
            if len(linia) > 0 :
                print( 'OK')
                lista1.append(linia[0])

    with open(f'imiona.txt','w') as imiona:
        for linia in lista1:
            linia = linia + '\n'
            imiona.write(linia)

imiona('meskie')
imiona('zenskie')

def names_list_create( file_name ):
    names_list = []
    with open(f'{file_name}.txt','r', encoding='utf-8') as imiona:
        names_list = [name.strip() for name in imiona.readlines()]
    return names_list

names_list = names_list_create('imiona')
print( names_list )
# Initialize list to store random dates
random_dates = []

# Define date range
start_date = datetime(1980, 1, 1)
end_date = datetime(2023, 12, 31)
# Difference between start and end dates
diff = end_date - start_date

# Generate 1000 random dates within the range
for _ in range(1000):
    random_seconds = random.randint(0, int(diff.total_seconds()))
    random_date = start_date + timedelta(seconds=random_seconds)
    random_dates.append(random_date)
    
# Generate 1 million objects
for i in range(1, 10001):
    # Each object is a dict with different types of data
    item = {
        'integer': i,
        'name': random.choice(names_list),  # Generate a random UUID as a string
        'date': str(random.choice(random_dates)),
        'float': round(random.random(),5),  # Generate a random float between 0.0 and 1.0
    }

    # Add the object to the data
    data.append(item)

# Write the data to a JSON file
with open('data.json', 'w') as f:
    json.dump(data, f)

