import random


def busqueda_lineal(lista, objetivo):
    match = False

    for elemento in lista:
        if elemento == objetivo:
            match = True
            break

    return match


if __name__ == "__main__":
    tamaño_lista = int(input("Ingrese el tamaño de la lista: "))
    objetivo = int(input("Ingrese el numero que desea buscar: "))

    lista = [random.randint(0, 100) for _ in range(tamaño_lista)]

    encontrado = busqueda_lineal(lista, objetivo)

    print(lista)
    print(f'el elemento {objetivo} {"esta" if encontrado else "no esta"} en la lista')
