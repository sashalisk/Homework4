"""
Sasha Lisk, Homework 4

Program tests five different hash function with 2 hash tables that create movie titles as keys and movie quotes as keys.
"""
# many collisions and unused buckets
#Sources: geeksforgeeks, w3schools, jane
"""
ATTEMPT 1: uses an ASCII sum hash function with separate chaining through linked lists.

The hash function adds the character values of each key and uses modulo to determine the bucket
If multiple keys hash to the same bucket then linked lists are used to store the records (THE BASE LINE)
"""


import csv
import time

# Hash function

def hash_function(key, table_size):

    total = 0

    for character in key:
        total += ord(character)

    return total % table_size

# Linked list node

class Node:

    def __init__(self, key, movie):

        self.key = key
        self.movies = [movie]
        self.next = None

# Linked list hash table

class HashTable:

    def __init__(self, size):

        self.size = size
        self.table = [None] * size

        self.collisions = 0
        self.records = 0
        self.unique_keys = 0

    def insert(self, key, movie):

        index = hash_function(key, self.size)

        current = self.table[index]

        if current is None:

            self.table[index] = Node(key, movie)

            self.records += 1
            self.unique_keys += 1

            return

        while current is not None:

            self.collisions += 1

            if current.key == key:

                current.movies.append(movie)
                self.records += 1

                return

            if current.next is None:

                current.next = Node(key, movie)

                self.records += 1
                self.unique_keys += 1

                return

            current = current.next

    def occupied(self):

        count = 0

        for bucket in self.table:

            if bucket is not None:
                count += 1

        return count

# Read in movies

def load_movies():

    movies = []

    with open("MOCK_DATA.csv", "r", newline="") as file:

        reader = csv.DictReader(file)

        for movie in reader:

            if movie["movie_title"] and movie["quote"]:
                movies.append(movie)

    return movies


# Statistics

def display_stats(name, table, elapsed):

    occupied = table.occupied()

    wasted = table.size - occupied

    load_factor = occupied / table.size

    print(name)
    print("------------------------------")


    print("Occupied buckets:", occupied)
    print("Wasted buckets:", wasted)
    print("Collisions:", table.collisions)
    print("Taken time:", round(elapsed, 6), "seconds")


# Main

def main():

    print("ATTEMPT 1: ASCII SUM + LINKED LISTS")

    movies = load_movies()


    size = len(movies) * 2 + 1

    # TITLE TABLE

    title_table = HashTable(size)

    start = time.perf_counter()

    for movie in movies:

        title_table.insert(
            movie["movie_title"].strip(),
            movie
        )

    end = time.perf_counter()

    display_stats(
        "MOVIE TITLE HASH TABLE",
        title_table,
        end - start
    )

    #  QUOTE TABLE

    quote_table = HashTable(size)

    start = time.perf_counter()

    for movie in movies:

        quote_table.insert(
            movie["quote"].strip(),
            movie
        )

    end = time.perf_counter()

    display_stats(
        "MOVIE QUOTE HASH TABLE",
        quote_table,
        end - start
    )


main()
