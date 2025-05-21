import math
import random
import numpy as np

def factorization(n):
    result = []
    
    for it in range(2, int(math.sqrt(n)) + 1):
        while n % it == 0 and n > 0:
            result.append(it)
            n //= it
    
    return result

def check(n, arr):
    arr.sort()
    ans = factorization(n)
    if len(arr) != len(ans):
        return False
    
    for i in range(len(arr)):
        if arr[i] != ans[i]:
            return False
    
    return True

def factorization_game():
    problems = [14, 15, 18, 16, 20, 21, 24, 26, 27, 28, 30, 34, 36, 38, 39, 40, 42, 44, 45, 46, 48, 49, 50, 51, 52, 54, 55, 56, 58, 60, 100, 112, 114, 115, 105, 72, 74, 78, 81, 84, 86, 88, 93, 63, 69, 64, 98, 99]
    q = random.choice(problems)
    print()
    print(f"Please factor the number {q}. \nExample input format for 12: \"2 2 3\"\n-------------------------------\nYour answer: ")
    resp = input()
    ans = np.fromstring(resp, dtype = int, sep = ' ')

    if(check(q, ans)):
        print("Congratulations! Your answer is correct!")
        return 20
    else:
        print("Sorry, your answer is incorrect.")
        return -10

if __name__ == "__main__":
    factorization_game()

    # for it in test_result:
    #     print(it, end = ' ')

    # print()
    # print(check(180, test_result))
    # print(check(165, test_result))