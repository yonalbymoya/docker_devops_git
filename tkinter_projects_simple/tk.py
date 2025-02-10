import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import sqlite3


def actualizar_subtotal(entradas, subtotal_var, iva_var, total_var):
    try:
        cantidad = float(entradas["Cantidad"].get() or 0)
        precio = float(entradas["Precio"].get() or 0)
        descuento = float(entradas["% Descuento"].get() or 0) / 100
        iva = float(iva_var.get() or 0) / 100
        subtotal = cantidad * precio * (1 - descuento)
        subtotal_var.set(f"{subtotal:.2f}")
        total = subtotal * (1 + iva)
        total_var.set(f"{total:.2f}")
    except ValueError:
        pass


def seleccionar_fecha(entry):
    def guardar_fecha():
        entry.delete(0, tk.END)
        entry.insert(0, cal.get_date())
        top.destroy()

    top = tk.Toplevel()
    cal = Calendar(top, selectmode="day", year=2025, month=2, day=9)
    cal.pack(pady=20)
    tk.Button(top, text="Seleccionar", command=guardar_fecha).pack()


def agregar_capitulo(frame_capitulos, contador, capitulos):
    capitulo = tk.Entry(frame_capitulos)
    capitulo.grid(row=len(capitulos), column=0, padx=5, pady=2, sticky="w")
    capitulos.append(capitulo)
    tk.Button(
        frame_capitulos,
        text="-",
        command=lambda: eliminar_capitulo(capitulo, capitulos),
    ).grid(row=len(capitulos) - 1, column=1, padx=5, pady=2)


def eliminar_capitulo(capitulo, capitulos):
    capitulo.destroy()
    capitulos.remove(capitulo)


def guardar_presupuesto(entradas, capitulos, subtotal_var, total_var):
    if not all(
        entradas[campo].get()
        for campo in ["Nombre", "Fecha", "Cantidad", "Unidad de Medida", "Precio"]
    ):
        messagebox.showerror(
            "Error", "Todos los campos son obligatorios excepto el descuento"
        )
        return

    conn = sqlite3.connect("presupuestos.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS presupuestos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            fecha TEXT,
            descripcion TEXT,
            cantidad REAL,
            unidad TEXT,
            precio REAL,
            descuento REAL,
            capitulos TEXT,
            subtotal REAL,
            total REAL
        )
    """
    )
    cursor.execute(
        """
        INSERT INTO presupuestos (nombre, fecha, descripcion, cantidad, unidad, precio, descuento, capitulos, subtotal, total)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            entradas["Nombre"].get(),
            entradas["Fecha"].get(),
            entradas["Descripción"].get(),
            entradas["Cantidad"].get(),
            entradas["Unidad de Medida"].get(),
            entradas["Precio"].get(),
            entradas["% Descuento"].get() or 0,
            ", ".join(capitulo.get() for capitulo in capitulos),
            subtotal_var.get(),
            total_var.get(),
        ),
    )
    conn.commit()
    conn.close()
    messagebox.showinfo("Éxito", "Presupuesto guardado con éxito")


def crear_presupuesto():
    ventana_presupuesto = tk.Toplevel()
    ventana_presupuesto.title("Crear Presupuesto")
    ventana_presupuesto.geometry("800x600")
    ventana_presupuesto.resizable(True, True)

    campos = [
        "Nombre",
        "Fecha",
        "Descripción",
        "Cantidad",
        "Unidad de Medida",
        "Precio",
        "% Descuento",
    ]
    entradas = {}

    frame = tk.Frame(ventana_presupuesto)
    frame.pack(padx=10, pady=10, fill="both", expand=True)

    for i, campo in enumerate(campos):
        row, col = divmod(i, 4)
        tk.Label(frame, text=campo).grid(
            row=row, column=col * 2, padx=5, pady=5, sticky="w"
        )
        entry = tk.Entry(frame)
        if campo == "Nombre":
            entry.insert(0, "PRE-")
        elif campo == "Fecha":
            tk.Button(
                frame, text="📅", command=lambda e=entry: seleccionar_fecha(e)
            ).grid(row=row, column=col * 2 + 2, padx=5)
        entry.grid(row=row, column=col * 2 + 1, padx=5, pady=5)
        entradas[campo] = entry

    tk.Label(frame, text="Capítulos").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    frame_capitulos = tk.Frame(frame)
    frame_capitulos.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky="w")
    capitulos = []
    tk.Button(
        frame,
        text="+",
        command=lambda: agregar_capitulo(frame_capitulos, [1], capitulos),
    ).grid(row=2, column=1, padx=5, pady=5)

    subtotal_var = tk.StringVar()
    iva_var = tk.StringVar()
    total_var = tk.StringVar()
    iva_entry = tk.Entry(frame, textvariable=iva_var)
    iva_entry.grid(row=5, column=3, padx=5, pady=5)
    iva_entry.bind(
        "<KeyRelease>",
        lambda e: actualizar_subtotal(entradas, subtotal_var, iva_var, total_var),
    )

    tk.Label(frame, text="Subtotal =").grid(row=4, column=2, padx=5, pady=5, sticky="e")
    tk.Label(frame, textvariable=subtotal_var).grid(
        row=4, column=3, padx=5, pady=5, sticky="w"
    )
    tk.Label(frame, text="IVA =").grid(row=5, column=2, padx=5, pady=5, sticky="e")
    tk.Label(frame, text="Total =").grid(row=6, column=2, padx=5, pady=5, sticky="e")
    tk.Label(frame, textvariable=total_var).grid(
        row=6, column=3, padx=5, pady=5, sticky="w"
    )

    tk.Button(
        frame,
        text="Guardar",
        bg="red",
        fg="white",
        command=lambda: guardar_presupuesto(
            entradas, capitulos, subtotal_var, total_var
        ),
    ).grid(row=7, column=2, columnspan=2, pady=10)


root = tk.Tk()
root.title("Administrativo")
root.geometry("300x200")

tk.Button(root, text="Crear Presupuesto", command=crear_presupuesto).pack(pady=10)
root.mainloop()
