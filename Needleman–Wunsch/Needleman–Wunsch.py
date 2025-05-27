# Meerza Ahmed 
# USC CSCI 570 Final Project
# python version 3.12.6 

"""
Notes : This project resembles the real world problem of DNA alignment. 
We need to create a new DNA strand from two sequences.
First solve the problem with a DP solution and follow up with an efficent solution minimizing cost of compute time and memory. 
"""

import sys
#from resource import *
import time
import psutil
import tracemalloc


def Alignment_func(seqX, seqY):
  
    # Hard code Gap penalty and Mismatch penalty 
    delta = 30
    alpha = {
        'A': {'A': 0,   'C': 110, 'G': 48,  'T': 94 },
        'C': {'A': 110, 'C': 0,   'G': 118, 'T': 48 },
        'G': {'A': 48,  'C': 118, 'G': 0,   'T': 110},
        'T': {'A': 94,  'C': 48,  'G': 110, 'T': 0  }
    }

    x, y = len(seqX), len(seqY)
    dp = [[0] * (y + 1) for _ in range(x + 1)]

    for i in range(1, x + 1):
        dp[i][0] = i * delta
        
    for j in range(1, y + 1):
        dp[0][j] = j * delta

    for i in range(1, x + 1):
        for j in range(1, y + 1):
            c1, c2 = seqX[i - 1], seqY[j - 1]
            
            match = dp[i - 1][j - 1] + alpha[c1][c2]
            gapX = dp[i - 1][j] + delta
            gapY = dp[i][j - 1] + delta
            
            dp[i][j] = min(match, gapX, gapY)

    newX, newY = [], []
    i, j = x, y
    
    while i > 0 and j > 0:
        c1, c2 = seqX[i - 1], seqY[j - 1]
        
        if dp[i][j] == dp[i - 1][j - 1] + alpha[c1][c2]:
            newX.append(c1)
            newY.append(c2)
            i -= 1
            j -= 1
            
        elif dp[i][j] == dp[i - 1][j] + delta:
            newX.append(c1)
            newY.append("_")
            i -= 1
            
        else:
            newX.append("_")
            newY.append(c2)
            j -= 1

    while i > 0:
        newX.append(seqX[i - 1])
        newY.append("_")
        i -= 1
        
    while j > 0:
        newX.append("_")
        newY.append(seqY[j - 1])
        j -= 1

    newX = ''.join(reversed(newX))
    newY = ''.join(reversed(newY))    
    cost = dp[x][y]   

    return newX, newY, cost

def process_memory(): # This did not work on my machine
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)
    return memory_consumed

def is_valid(start_len, indices, end_len):
    check_len = (2 ** indices) * start_len
    return end_len == check_len

def generate_str(seq_str, indices):
    
    s = seq_str
    for i in indices:
        s = s[:i + 1] + s + s[i + 1:]

    if not is_valid(len(seq_str), len(indices), len(s)):
        raise ValueError("string length is incorrect")

    return s


def time_wrapper(seqX,seqY):
    
    tracemalloc.start()
    start_time = time.time()
    
    newX, newY, cost = Alignment_func(seqX, seqY)
    _, peak = tracemalloc.get_traced_memory()
    
    tracemalloc.stop()
    end_time = time.time()
    
    time_taken = (end_time - start_time)*1000
    total_memory = peak / 1024  
    
    return newX, newY, cost, time_taken, total_memory

def R_input(input_f):
   
    with open(input_f, 'r') as f:
        strX = f.readline().strip()
        indicesX = []
        
        while True:
            line = f.readline().strip()
            if not line or not line.isdigit():
                strY = line
                break
            indicesX.append(int(line))
        
        indicesY = []
        for line in f:
            line = line.strip()
            if line and line.isdigit():
                indicesY.append(int(line))

    seqX = generate_str(strX, indicesX)    
    seqY = generate_str(strY, indicesY)
    return seqX, seqY

def W_output(output_f, cost, newX, newY, total_time, total_memory):
    
    with open(output_f, "w") as f:
        f.write(f"{cost}\n")
        f.write(f"{newX}\n")
        f.write(f"{newY}\n")
        f.write(f"{total_time}\n")
        f.write(f"{total_memory}\n")
        f.close()

if __name__ == "__main__":
    
    if len(sys.argv) < 3:
        print("Usage: python3 basic_3.py inputFile.txt outputFile.txt")
        sys.exit()
        
    input_f  = sys.argv[1]
    output_f = sys.argv[2]

    seqX, seqY = R_input(input_f)
    newX, newY, cost, total_time, total_memory = time_wrapper(seqX, seqY)
    
    #total_memory = process_memory()
    
    W_output(output_f, cost, newX, newY, total_time, total_memory)
    