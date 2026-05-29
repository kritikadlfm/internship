''' practice questions 
Store your name, age, and favourite programming language in variables
Print this sentence using an f-string:
"Hi, I'm Arjun, I'm 22 years old and I love Python."
Take the string "  modern python  " and print it stripped and uppercased in one line
Given a = 17 and b = 5, print the quotient and remainder of dividing a by b'''
name="Kritika Dadheech"
age=21
prog_language="Python"
print(f"Hi, I am {name}, I'm {age} years old and I love {prog_language}")
s=input("enter a string")
s=s.strip().upper()
print(s)
a=17
b=5
print("Quotient:",a/b)
print("Remainder:",a%b)
'''Exercise 2
Write a program that:

Asks the user to input a number
Converts it to an integer
Prints whether it is:

"Positive and even"
"Positive and odd"
"Negative"
"Zero"


Bonus: also print "Divisible by both 3 and 5" if it applies'''
num = input("enter an integer")
num = int(num)
if (num > 0  and num % 2 == 0):
    print("Positive and Even")
elif (num > 0 and num % 2!= 0):
    print("Positive and Odd")
elif (num < 0):
    print("Negative")
else:
    print("Zero")
if(num % 3 == 0 and num % 5== 0):
    print("Divisible by both 3 and 5")
''' Exercise 3
Write a program that:

Prints a multiplication table for a number entered by the user (1 to 10)
Uses a while loop to keep asking the user for a number until they type "quit"
For each number, also print which results in the table are divisible by 3'''
while(True):
    user_input = input("enter a number (or quit to exit): ")
    if user_input == "quit":
        print("Goodbye !")
        break
    n=int(user_input)
    for i in range (1,11):
        result = n * i
        suffix = " <-- divisible by 3 " if result % 3 == 0 else ""
        print(f"{n} x {i} = {result}{suffix}") 
'''Exercise 4
Write a program that:

Stores a list of 5 students, each as a dictionary with name, age, and grade (0–100)
Prints only students who passed (grade >= 50)
Prints the highest grade and which student got it
Prints all student names in alphabetical order''' 
students = [
    {"name": "Kritika", "age": 21, "grade": 88},
    {"name": "Arjun",   "age": 22, "grade": 45},
    {"name": "Sneha",   "age": 20, "grade": 76},
    {"name": "Rohan",   "age": 23, "grade": 33},
    {"name": "Priya",   "age": 21, "grade": 91}
]
print("Passed students")
for student in students:
    if student["grade"] >= 50:
        print(f"{student["name"]} - {student["grade"]}")
print("Highest Grade")
topper=max(students, key=lambda s : s["grade"])
print(f"{topper ['name']} with {topper['grade']}")
print("alphabetical order")
for student in sorted(students, key = lambda s: s["name"]):
    print(student['name'])


    