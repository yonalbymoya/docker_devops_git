import os
import re


class ReadLogsLines:
    def __init__(self):
        pass

    def read_logs(self):
        with os.popen("ls -l") as f:
            contenido = f.read()
            print("Estos archivos estan en el directorio actual\n", contenido)

    def read_lines(self, file_path):
        with open(file_path, "r") as archivo:
            for linea in archivo:
                if linea:
                    print(linea)
                else:
                    print("No hay lineas en el archivo")

    def search_lines(self, file_path, objetivo):
        objetivo = objetivo.lower()
        print(f"Buscando '{objetivo}' en el archivo {file_path}")
        words = 0
        with open(file_path, "r") as archivo:
            for word, linea in enumerate(archivo):
                if linea.startswith(objetivo):
                    words += 1
                    print(f"Hay {words} palabras {objetivo} en el archivo")
            return "No hay palabras {objetivo} en el archivo"


if __name__ == "__main__":
    rll = ReadLogsLines()
    rll.read_logs()

    file_path = input("Ingrese el nombre del archivo: ")
    objetivo = input("Ingrese la palabra que quiere buscar: ")
    if os.path.exists(file_path):
        if objetivo:
            rll.search_lines(file_path, objetivo)
        else:
            rll.read_lines(file_path)
        print("Archivo leido")
    else:
        print(f"El archivo {file_path} no existe en la ruta actual")
