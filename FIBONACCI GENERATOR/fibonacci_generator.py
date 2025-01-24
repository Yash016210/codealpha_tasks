def fibonacci_generator():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Usage:
if __name__ == "__main__":
    n = int(input("Enter the number of terms: "))
    fib_gen = fibonacci_generator()
    for _ in range(n):
        print(next(fib_gen))
