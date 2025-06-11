#!/usr/bin/env python3
"""
Python Sequences Examples
Different ways to create sequences in Python
"""

import matplotlib.pyplot as plt

# 1. LIST SEQUENCES
print("=== LIST SEQUENCES ===")

# Simple list
numbers = [1, 2, 3, 4, 5]
print(f"Simple list: {numbers}")

# List with range
range_list = list(range(1, 11))  # 1 to 10
print(f"Range list: {range_list}")

# List with step
step_list = list(range(0, 21, 2))  # Even numbers 0 to 20
print(f"Step list: {step_list}")

# List comprehension
squares = [x**2 for x in range(1, 6)]
print(f"Squares: {squares}")

# 2. TUPLE SEQUENCES
print("\n=== TUPLE SEQUENCES ===")

# Simple tuple
coordinates = (10, 20, 30)
print(f"Coordinates: {coordinates}")

# Tuple from range
tuple_range = tuple(range(5, 10))
print(f"Tuple range: {tuple_range}")

# 3. STRING SEQUENCES
print("\n=== STRING SEQUENCES ===")

# String as sequence
text = "Hello World"
print(f"String: {text}")
print(f"Characters: {list(text)}")

# Generate alphabet sequence
alphabet = ''.join(chr(ord('a') + i) for i in range(26))
print(f"Alphabet: {alphabet}")

# 4. NUMPY SEQUENCES (if numpy is available)
print("\n=== NUMPY SEQUENCES ===")
try:
    import numpy as np
    
    # Linear sequence
    linear = np.linspace(0, 10, 11)  # 11 points from 0 to 10
    print(f"Linear sequence: {linear}")
    
    # Arithmetic sequence
    arithmetic = np.arange(0, 10, 0.5)  # 0 to 10 with step 0.5
    print(f"Arithmetic sequence: {arithmetic}")
    
    # Geometric sequence
    geometric = np.logspace(0, 2, 5)  # 5 points from 10^0 to 10^2
    print(f"Geometric sequence: {geometric}")
    
except ImportError:
    print("NumPy not available - install with: pip install numpy")

# 5. CUSTOM SEQUENCES
print("\n=== CUSTOM SEQUENCES ===")

# Fibonacci sequence
def fibonacci(n):
    """Generate first n Fibonacci numbers"""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib

fib_sequence = fibonacci(10)
print(f"Fibonacci: {fib_sequence}")

# Prime numbers sequence
def primes(n):
    """Generate first n prime numbers"""
    primes_list = []
    num = 2
    while len(primes_list) < n:
        is_prime = True
        for p in primes_list:
            if p * p > num:
                break
            if num % p == 0:
                is_prime = False
                break
        if is_prime:
            primes_list.append(num)
        num += 1
    return primes_list

prime_sequence = primes(10)
print(f"First 10 primes: {prime_sequence}")

# 6. SEQUENCES WITH PATTERNS
print("\n=== PATTERN SEQUENCES ===")

# Alternating sequence
alternating = [1 if i % 2 == 0 else -1 for i in range(10)]
print(f"Alternating: {alternating}")

# Factorial sequence
factorials = []
factorial = 1
for i in range(1, 8):
    factorial *= i
    factorials.append(factorial)
print(f"Factorials: {factorials}")

# Powers of 2
powers_of_2 = [2**i for i in range(10)]
print(f"Powers of 2: {powers_of_2}")

# 7. ITERTOOLS SEQUENCES
print("\n=== ITERTOOLS SEQUENCES ===")
import itertools

# Infinite sequence (take only first 10)
count_seq = list(itertools.islice(itertools.count(1, 2), 10))  # Odd numbers
print(f"Count sequence: {count_seq}")

# Cycle sequence
cycle_seq = list(itertools.islice(itertools.cycle(['A', 'B', 'C']), 10))
print(f"Cycle sequence: {cycle_seq}")

# Repeat sequence
repeat_seq = list(itertools.repeat('X', 5))
print(f"Repeat sequence: {repeat_seq}")

# 8. SEQUENCES FOR DATA SCIENCE
print("\n=== DATA SCIENCE SEQUENCES ===")

# Time series dates
from datetime import datetime, timedelta

start_date = datetime(2025, 1, 1)
date_sequence = [start_date + timedelta(days=i) for i in range(7)]
print(f"Date sequence: {[d.strftime('%Y-%m-%d') for d in date_sequence]}")

# Random sequences
import random

random.seed(42)  # For reproducibility
random_seq = [random.randint(1, 100) for _ in range(10)]
print(f"Random sequence: {random_seq}")

# Normal distribution (if numpy available)
try:
    np.random.seed(42)
    normal_seq = np.random.normal(0, 1, 10).round(2)
    print(f"Normal distribution: {normal_seq}")
except:
    print("NumPy not available for normal distribution")

print("\n=== SEQUENCE OPERATIONS ===")

# Common sequence operations
seq = [1, 2, 3, 4, 5]
print(f"Original: {seq}")
print(f"Length: {len(seq)}")
print(f"Sum: {sum(seq)}")
print(f"Min: {min(seq)}")
print(f"Max: {max(seq)}")
print(f"Reversed: {list(reversed(seq))}")
print(f"Sorted: {sorted(seq, reverse=True)}")

# Slicing
print(f"First 3: {seq[:3]}")
print(f"Last 2: {seq[-2:]}")
print(f"Every 2nd: {seq[::2]}")
