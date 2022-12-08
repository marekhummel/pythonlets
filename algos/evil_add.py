from time import sleep, perf_counter


num1 = 2
num2 = 4

zero = perf_counter()
sleep(num1)
sleep(num2)
result = perf_counter() - zero

print(result)
