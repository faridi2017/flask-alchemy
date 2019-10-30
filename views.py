from run import app
from flask import jsonify
@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})




'''
str.isdigit() (Decimals, Subscripts, Superscripts)
str.isdecimal() (Only Decimal Numbers, no superscript,subscript)
'a1'.isalpha(), 'a1'.isdigit(), 'a1'.isalnum()
(False, False, True)
str.isalnum()
Return true if all characters in the string are alphanumeric and there is at least one character, 
false otherwise. A character c is alphanumeric if one the following returns True: c.isalpha(), c.isdecimal(), c.isdigit(), or c.isnumeric().

The isdigit() returns:

True if all characters in the string are digits.
False if at least one character is not a digit.

str.isnumeric, behaving differently from their 0-9 counterparts(in other languagees)
---------------------
input = 'this is reddit learn python'
>>> output = input.split()
>>> output
['this', 'is', 'reddit', 'learn', 'python']
-------------------
# Python program to Count Alphabets Digits and Special Characters in a String
 
string = input("Please Enter your Own String : ")
alphabets = digits = special = 0

for i in range(len(string)):
    if(string[i].isalpha()):
        alphabets = alphabets + 1
    elif(string[i].isdigit()):
        digits = digits + 1
    else:
        special = special + 1
        
print("\nTotal Number of Alphabets in this String :  ", alphabets)
print("Total Number of Digits in this String :  ", digits)
print("Total Number of Special Characters in this String :  ", special)
-------------------------------
test_str = "GeeksforGeeks"
  
# using naive method to get count  
# of each element in string  
all_freq = {} 
  
for i in test_str: 
    if i in all_freq: 
        all_freq[i] += 1
    else: 
        all_freq[i] = 1
  
# printing result  
print ("Count of all characters in GeeksforGeeks is :\n "
                                        +  str(all_freq)) 
Output :

Count of all characters in GeeksforGeeks is :
 {'r': 1, 'e': 4, 'k': 2, 'G': 2, 's': 2, 'f': 1, 'o': 1}
 ---------------------------
 from collections import Counter 
  
# initializing string  
test_str = "GeeksforGeeks"
  
# using collections.Counter() to get  
# count of each element in string  
res = Counter(test_str) 
  
# printing result  
print ("Count of all characters in GeeksforGeeks is :\n "
                                           +  str(res)) 
-----------------------------------------------------
MYSQL
_________
Using simple GROUP_CONCAT() function-
SELECT emp_id, fname, lname, dept_id, 
GROUP_CONCAT ( strength ) as "strengths" 
FROM employee group by emp_id;

'''