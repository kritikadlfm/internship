numbers = [1, 2, 3, 4, 5]

squares = [num ** 2 for num in numbers]

print(squares)


try:
    number = int(input("Enter a number: "))
    print(number)
except ValueError:
    print("Invalid input")