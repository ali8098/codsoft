import random
import string

def password_generation(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password
def generator():
    print("Password Generator")
    while True:
        length = int(input("Enter the desired length of the password: "))
        if length <= 0:
            print("Invalid entry. Please enter a positive integer.")
            continue
        password = password_generation(length)
        print("Generated Password:", password)
        answer = input("Do you want to generate another password? (yes/no): ").lower()
        if answer != "yes":
            print("Exiting the password generator.")
            break

if __name__ == "__main__":
    generator()
