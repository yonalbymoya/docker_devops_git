import time


def factorial(n):
    respuesta = 1

    while n > 1:
        respuesta *= n
        n -= 1

    return respuesta


def factorial_recursivo(n):
    if n == 1:
        return 1

    return n * factorial(n - 1)


if __name__ == "__main__":
    start = time.time()
    factorial(100000)
    finish = time.time()
    print(f"Tiempo de ejecución: {finish - start}")

    start = time.time()
    factorial_recursivo(100000)
    finish = time.time()
    print(f"Tiempo de ejecución: {finish - start}")
