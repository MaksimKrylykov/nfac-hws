"""
Exercise 1:
Create a Pizza class that could have ingredients added to it. Raise an error if an attempt is made to add a duplicate ingredient.
"""
class Pizza:
    def __init__(self):
        self.ingredients = set()

    def add_ingredient(self, ingredient):
        if ingredient in self.ingredients:
            raise ValueError("This ingredient is already used")
        self.ingredients.add(ingredient)


"""
Exercise 2:
Create an Elevator class with methods to go up, go down, and get the current floor. The elevator should not be able to go below the ground floor (floor 0).
"""
class Elevator:
    def __init__(self):
        self.floor = 0

    def go_up(self):
        self.floor += 1

    def go_down(self):
        if self.floor > 0:
            self.floor -= 1

    def get_current_floor(self):
        return self.floor


"""
Exercise 3:
Create a class Stack with methods to push, pop, and check if the stack is empty. Raise an exception if a pop is attempted on an empty stack.
"""
class Stack:
    def __init__(self):
        self.stack = list()

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.stack.pop()

    def is_empty(self):
        return len(self.stack) == 0


"""
Exercise 4:
Design a BankAccount class with methods to deposit, withdraw, and check balance. Ensure that an account cannot go into a negative balance.
"""
class BankAccount:
    def __init__(self, initial_balance):
        self.balance = initial_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance < amount:
            raise ValueError("Not enough money on balance")
        else:
            self.balance -= amount

    def check_balance(self):
        return self.balance


"""
Exercise 5:
Create a class Person with attributes for name and age. Implement a method birthday that increases the person's age by one. Raise an exception if an age less than 0 is entered.
"""
class Person:
    def __init__(self, name, age):
        if age < 0:
            raise ValueError("You still haven't born yet")
        self.name = name
        self.age = age

    def birthday(self):
        self.age += 1


"""
Exercise 6:
Create an Animal base class and a Dog and Cat derived classes. Each animal should have a sound method which returns the sound they make.
"""
class Animal:
    def sound(self):
        return "Weird noises"

class Dog(Animal):
    def sound(self):
        return "Woof"

class Cat(Animal):
    def sound(self):
        return "Meow"


"""
Exercise 7:
Design a class Calculator with static methods for addition, subtraction, multiplication, and division. Division method should raise a ZeroDivisionError when trying to divide by zero.
"""
class Calculator:
    @staticmethod
    def add(x, y):
        return x + y

    @staticmethod
    def subtract(x, y):
        return x - y

    @staticmethod
    def multiply(x, y):
        return x * y

    @staticmethod
    def divide(x, y):
        if y == 0:
            raise ZeroDivisionError("bruh.")
        return x // y


"""
Exercise 8:
Create a class `Car` with attributes for speed and mileage. Raise a ValueError if a negative value for speed or mileage is entered.
"""
class Car:
    def __init__(self, speed, mileage):
        if speed < 0 or mileage < 0:
            raise ValueError("No negatives in my car")
        self.speed = speed
        self.mileage = mileage


"""
Exercise 9:
Create a Student class and a Course class. Each Course can enroll students and print a list of enrolled students.
"""
class Student:
    def __init__(self, name):
        self.name = name

class Course:
    def __init__(self):
        self.enrolled = set()

    def enroll(self, student):
        self.enrolled.add(student)

    def print_students(self):
        for i in self.enrolled:
            print(i.name)


"""
Exercise 10:
Create a Flight class with a destination, departure time, and a list of passengers. Implement methods to add passengers, change the destination, and delay the flight by a certain amount of time.
"""
class Flight:
    def __init__(self, destination, departure):
        self.passengers = set()
        self.destination = destination
        self.departureHoursMins = [int(departure[0:2]), int(departure[3:5])]
        self.departure = departure

    def add_passenger(self, passenger):
        self.passengers.add(passenger)

    def change_destination(self, new_destination):
        self.destination = new_destination

    def delay(self, delay_time):
        self.departureHoursMins[0] += delay_time
        self.departureHoursMins[0] %= 24
        self.departure = ("0" if self.departureHoursMins[0] < 10 else "") + str(self.departureHoursMins[0]) + ':'
        self.departure += ("0" if self.departureHoursMins[1] < 10 else "") + str(self.departureHoursMins[1])


"""
Exercise 11:
Create a Library class with a list of Book objects. The Book class should have attributes for title and author. The Library class should have methods to add books and find a book by title.
"""
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def find_by_title(self, title):
        for i in self.books:
            if i.title == title:
                return i
        print("No books found")


"""
Exercise 12:
Design a class Matrix that represents a 2D matrix with methods for addition, subtraction, and multiplication. Implement error handling for operations that are not allowed (e.g., adding matrices of different sizes).
"""
class Matrix:
    def __init__(self, matrix):
        if not(matrix):
            raise Exception("No empty matrices")

        self.n = len(matrix)
        if (type(matrix[0]) != type([])):
            raise Exception("Must be a 2D matrix")

        self.m = len(matrix[0])
        for i in range(self.n):
            if (type(matrix[i]) != type([])):
                raise Exception("Must be a 2D matrix")

            if (len(matrix[i]) != self.m):
                raise Exception("Must be a matrix")

            for j in range(self.m):
                if type(matrix[i][j]) != type(0) and type(matrix[i][j]) != type(0.0):
                    raise Exception("Must be a 2D matrix")

        self.matrix = matrix

    def add(self, other):
        if self.n != other.n or self.m != other.m:
            raise Exception("Can't add")

        result = [[0 for j in range(self.m)] for i in range(self.n)]
        for i in range(self.n):
            for j in range(self.m):
                result[i][j] = self.matrix[i][j] + other.matrix[i][j]

        return Matrix(result)


    def subtract(self, other):
        if self.n != other.n or self.m != other.m:
            raise Exception("Can't subtract")

        result = [[0 for j in range(self.m)] for i in range(self.n)]
        for i in range(self.n):
            for j in range(self.m):
                result[i][j] = self.matrix[i][j] - other.matrix[i][j]

        return Matrix(result)

    def multiply(self, other):
        if self.m != other.n:
            raise Exception("Can't multiply")

        result = [[0 for j in range(other.m)] for i in range(self.n)]
        for i in range(self.n):
            for j in range(other.m):
                for k in range(self.m):
                    result[i][j] += self.matrix[i][k] * other.matrix[k][j]

        return Matrix(result)


"""
Exercise 13:
Create a class Rectangle with attributes for height and width. Implement methods for calculating the area and perimeter of the rectangle. Also, implement a method is_square that returns true if the rectangle is a square and false otherwise.
"""
class Rectangle:
    def __init__(self, height, width):
        self.height = height
        self.width = width

    def area(self):
        return self.height * self.width

    def perimeter(self):
        return 2 * (self.height + self.width)

    def is_square(self):
        return self.height == self.width


"""
Exercise 14:
Design a class Circle with attributes for radius. Implement methods for calculating the area and the circumference of the circle. Handle exceptions for negative radius values.
"""
class Circle:
    def __init__(self, radius):
        if radius < 0:
            raise ValueError("No negatives in my house")
        self.radius = radius

    def area(self):
        from math import pi
        return pi * self.radius ** 2

    def circumference(self):
        from math import pi
        return 2 * pi * self.radius


"""
Exercise 15:
Design a class Triangle with methods to calculate the area and perimeter. Implement error handling for cases where the given sides do not form a valid triangle.
"""
class Triangle:
    def __init__(self, side_a, side_b, side_c):
        if side_a <= 0 or side_b <= 0 or side_c <= 0:
            raise ValueError("No negatives in my house")

        if side_a + side_b <= side_c:
            raise ValueError("Invalid triangle")

        if side_a + side_c <= side_b:
            raise ValueError("Invalid triangle")

        if side_b + side_c <= side_a:
            raise ValueError("Invalid triangle")

        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c

    def area(self):
        p = self.perimeter() / 2
        return (p * (p - self.side_a) * (p - self.side_b) * (p - self.side_c)) ** 0.5

    def perimeter(self):
        return self.side_a + self.side_b + self.side_c


"""
Exercise 16:
Design a class Triangle with methods to calculate the area and perimeter. Implement error handling for cases where the given sides do not form a valid triangle.
"""
class AbstractShape:
    def area(self):
        return 0

    def perimeter(self):
        return 0


class Circle(AbstractShape):
    def __init__(self, radius):
        if radius < 0:
            raise ValueError("No negatives in my house")
        self.radius = radius

    def area(self):
        from math import pi
        return pi * self.radius ** 2

    def circumference(self):
        from math import pi
        return 2 * pi * self.radius


class Rectangle(AbstractShape):
    def __init__(self, height, width):
        self.height = height
        self.width = width

    def area(self):
        return self.height * self.width

    def perimeter(self):
        return 2 * (self.height + self.width)

    def is_square(self):
        return self.height == self.width


class Triangle(AbstractShape):
    def __init__(self, side_a, side_b, side_c):
        if side_a <= 0 or side_b <= 0 or side_c <= 0:
            raise ValueError("No negatives in my house")

        if side_a + side_b <= side_c:
            raise ValueError("Invalid triangle")

        if side_a + side_c <= side_b:
            raise ValueError("Invalid triangle")

        if side_b + side_c <= side_a:
            raise ValueError("Invalid triangle")

        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c

    def area(self):
        p = self.perimeter() / 2
        return (p * (p - self.side_a) * (p - self.side_b) * (p - self.side_c)) ** 0.5

    def perimeter(self):
        return self.side_a + self.side_b + self.side_c


"""
Exercise 17:
Create a MusicPlayer class that contains a list of songs and methods to add songs, play a song, and skip to the next song. Also implement a method to shuffle the playlist.
"""
class MusicPlayer:
    def __init__(self):
        self.playlist = []
        self.pointer = 0
        self.current_song = None

    def add_song(self, song):
        self.playlist.append(song)

    def play_song(self):
        if len(self.playlist) == 0:
            pass
        self.current_song = self.playlist[self.pointer]

    def next_song(self):
        if len(self.playlist) == 0:
            pass
        self.pointer += 1
        self.pointer %= len(self.playlist)
        self.current_song = self.playlist[self.pointer]

    def shuffle(self):
        from random import shuffle
        shuffle(self.playlist)
        self.pointer = 0
        self.current_song = self.playlist[self.pointer]


"""
Exercise 18:
Design a Product class for an online store with attributes for name, price, and quantity. Implement methods to add stock, sell product, and check stock levels. Include error handling for attempting to sell more items than are in stock.
"""
class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def add_stock(self, quantity):
        self.quantity += quantity

    def sell(self, quantity):
        if self.quantity < quantity:
            raise ValueError("Can't sell more than I have")
        self.quantity -= quantity

    def check_stock(self):
        return self.quantity * self.price


"""
Exercise 19:
Create a VideoGame class with attributes for title, genre, and rating. Implement methods to change the rating, change the genre, and display game details.
"""
class VideoGame:
    def __init__(self, title, genre, rating):
        self.title = title
        self.genre = genre
        self.rating = rating

    def change_rating(self, rating):
        self.rating = rating

    def change_genre(self, genre):
        self.genre = genre

    def display_details(self):
        print(f"{self.title} video game. Genre: {self.genre}, rating : {self.rating}.")


"""
Exercise 20:
Create a School class with a list of Teacher and Student objects. Teacher and Student classes should have attributes for name and age. The School class should have methods to add teachers, add students, and print a list of all people in the school.
"""
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Teacher(Person):
    pass

class Student(Person):
    pass

class School:
    def __init__(self):
        self.teachers = []
        self.students = []

    def add_teacher(self, teacher):
        self.teachers.append(teacher)

    def add_student(self, student):
        self.students.append(student)

    def get_all(self):
        return self.teachers + self.students


"""
Exercise 21:
Design a Card class to represent a playing card with suit and rank. Then design a Deck class that uses the Card class. The Deck class should have methods to shuffle the deck, deal a card, and check the number of remaining cards.
"""
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

class Deck:
    def __init__(self):
        self.cards = []
        for i in range(1, 14):
            rank = str(i)
            if rank == '1':
                rank = 'Ace'
            elif rank == '11':
                rank = 'Jack'
            elif rank == '12':
                rank = 'Queen'
            elif rank == '13':
                rank = 'King'
            self.cards.append(Card("Spades", rank))
            self.cards.append(Card("Hearts", rank))
            self.cards.append(Card("Diamonds", rank))
            self.cards.append(Card("Clubs", rank))

    def shuffle(self):
        from random import shuffle
        shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

    def count(self):
        return len(self.cards)
