# Factorial: Implementa una función recursiva para calcular el factorial de un número.


def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


# Fibonacci: Calcula el n-ésimo número de la serie de Fibonacci usando recursión.


def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


# Suma de dígitos: Crea una función recursiva que reciba un número y devuelva la suma de sus dígitos.


def sum_digits_(n):
    if n > 0:
        return sum(range(n))
    else:
        return 0


# Potencia: Escribe una función recursiva que calcule la potencia de un número (base y exponente como argumentos).


def power(base, exponent):
    if exponent == 0:
        return 1
    else:
        print("Esto es ", base, "-", power(base, exponent - 1))
        return base * power(base, exponent - 1)


print(power(2, 3))
