"""
Sasha Lisk, Homework 4,

Program tests five different hash function with 2 hash tables that create movie titles as keys and movie quotes as keys.
"""
#I reduced the hash table size to target a load factor of approximately 0.65 instead of 0.50.
#this method to reduce wasted space and test how changing the multiplier and table size affects collisions and speed
"""
ATTEMPT 5: IMPROVED POLYNOMIAL HASHING
Polynomial hashing with multiplier 37 and linear probing reduce wasted space while good hash table performance (changes table size)
"""

import csv
import time


# Hash func

def hash_function(key, table_size):

    total = 0

    for character in key:

        total = (total * 37 + ord(character)) % table_size

    return total


# hash table

class HashTable:

    def __init__(self, size):

        self.size = size
        self.table = [None] * size

        self.collisions = 0
        self.records = 0
        self.unique_keys = 0

    def insert(self, key, movie):

        index = hash_function(key, self.size)

        for attempt in range(self.size):

            if self.table[index] is None:

                self.table[index] = [key, [movie]]

                self.records += 1
                self.unique_keys += 1

                return

            self.collisions += 1

            if self.table[index][0] == key:

                self.table[index][1].append(movie)

                self.records += 1

                return

            index = (index + 1) % self.size

        raise RuntimeError("Hash table is full!")

    def occupied(self):

        count = 0

        for slot in self.table:

            if slot is not None:
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


# Stats

def display_stats(name, table, elapsed):

    occupied = table.occupied()

    wasted = table.size - occupied

    print(name)
    print("------------------------------")


    print("Occupied slots:", occupied)
    print("Wasted slots:", wasted)
    print("Collisions:", table.collisions)
    print("Tracker time:", round(elapsed, 6), "seconds")


# Main

def main():

    print("ATTEMPT 5: IMPROVED POLYNOMIAL HASHING")

    movies = load_movies()

    # Target a load factor of approximately 0.65
    size = int(len(movies) / 0.65) + 1

    # TITLE TABLE

    title_table = HashTable(size)

    start = time.perf_counter()

    for movie in movies:

        title_table.insert(movie["movie_title"].strip(), movie)

    end = time.perf_counter()

    display_stats("MOVIE TITLE HASH TABLE", title_table, end - start)

    # QUOTE TABLE

    quote_table = HashTable(size)

    start = time.perf_counter()

    for movie in movies:

        quote_table.insert(movie["quote"].strip(), movie)

    end = time.perf_counter()

    display_stats("MOVIE QUOTE HASH TABLE", quote_table, end - start)


main()
