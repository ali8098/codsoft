import math as mt

class Calculator:
    def add(self,x,y):
        return x + y
    
    def sub(self,x,y):
        return x - y
    
    def mul(self,x,y):
        return x * y
    
    def div(self,x,y):
        if y == 0:
            print("Error in division input")
        else:
            return x / y
    
    def power(self,x,y):
        return x ** y
    
    def square_root(self,x):
        if x < 0:
            return "Error in operation"
        else:
            return mt.sqrt(x)
    
    def factorial(self, x):
        return mt.factorial(x)    

calculator = Calculator()

while True:
    print("*************************CALCULATOR*************************")

    print("Select operation of your own choice" )
    print("1)Addition\n2)Subtract\n3)Divide\n4)Multiply\n5)Power\n6)square root\n7)Factorial\n8)Exit")

    choice=input("")
    if choice in ('1', '2', '3', '4'):
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        if choice == "1":
            print("Result:", calculator.add(num1, num2))
        if choice == "2":
            print("Result:", calculator.sub(num1, num2))
        if choice == "3":
            print("Result:", calculator.div(num1, num2))
        if choice == "4":
            print("Result:", calculator.mul(num1, num2))

    elif choice=="5":
        num1=float(input("Enter base:"))
        num2=float(input("Enter exponent:"))
        print("Result:", calculator.power(num1, num2))
    elif choice == '6':
        num = float(input("Enter number: "))
        print("Result:", calculator.square_root(num))
    elif choice == '7':
        num = int(input("Enter number: "))
        print("Result:", calculator.factorial(num))
    elif choice == '8':
        print("Exiting the calculator. Goodbye!")
        break
    else:
        print("Invalid input. Please enter a valid choice.")
