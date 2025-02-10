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


def agregar_capitulo(frame_capitulos, capitulos):
    frame = tk.Frame(frame_capitulos)
    frame.grid(row=len(capitulos), column=0, columnspan=2, padx=5, pady=2, sticky="w")

    capitulo = tk.Entry(frame)
    capitulo.pack(side="left")

    btn_eliminar = tk.Button(
        frame, text="-", command=lambda: eliminar_capitulo(frame, capitulos)
    )
    btn_eliminar.pack(side="left", padx=5)

    capitulos.append(
        capitulo
    )  # Guardamos el frame en la lista para poder eliminarlo correctamente


def eliminar_capitulo(frame, capitulos):
    if capitulos:
        frame.destroy()
        capitulos.remove(frame)
    else:
        messagebox.showerror("Error", "No hay capitulos para")


def guardar_presupuesto(entradas, capitulos, subtotal_var, iva_var, total_var):
    if not all(
        entradas[campo].get()
        for campo in [
            "Nombre Proveedor",
            "Nombre Presupuesto",
            "Fecha",
            "Cantidad",
            "Unidad de Medida",
            "Precio",
        ]
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
            nombre_proveedor TEXT,
            nombre_presupuesto TEXT,
            fecha TEXT,
            descripcion TEXT,
            cantidad REAL,
            unidad TEXT,
            precio REAL,
            descuento REAL,
            capitulos TEXT,
            subtotal REAL,
            iva REAL,
            total REAL
        )
    """
    )
    cursor.execute(
        """
        INSERT INTO presupuestos (nombre, fecha, descripcion, cantidad, unidad, precio, descuento, capitulos, subtotal, iva, total)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            entradas["Nombre Proveedor"].get(),
            entradas["Nombre Presupuesto"].get(),
            entradas["Fecha"].get(),
            entradas["Descripción"].get(),
            entradas["Cantidad"].get(),
            entradas["Unidad de Medida"].get(),
            entradas["Precio"].get(),
            entradas["% Descuento"].get() or 0,
            ", ".join(capitulo.get() for capitulo in capitulos),
            subtotal_var.get(),
            iva_var.get(),
            total_var.get(),
        ),
    )
    conn.commit()
    conn.close()
    messagebox.showinfo("Éxito", "Presupuesto guardado con éxito")


def crear_presupuesto():
    ventana_presupuesto = tk.Toplevel()
    ventana_presupuesto.title("Crear Presupuesto")
    ventana_presupuesto.geometry("1080x600")
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
            entry.grid(row=row, column=col * 2 + 1, padx=5, pady=5)
            tk.Button(
                frame, text="📅", command=lambda e=entry: seleccionar_fecha(e)
            ).grid(
                row=row, column=col * 2 + 2, padx=5, pady=5, sticky="w"
            )  # Agregado sticky="w"

        entry.grid(row=row, column=col * 2 + 1, padx=5, pady=5)
        entradas[campo] = entry

    tk.Label(frame, text="Capítulos").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    frame_capitulos = tk.Frame(frame)
    frame_capitulos.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky="w")
    capitulos = []
    tk.Button(
        frame,
        text="+",
        command=lambda: agregar_capitulo(frame_capitulos, capitulos),
    ).grid(row=2, column=1, padx=5, pady=5)

    subtotal_var = tk.StringVar()
    iva_var = tk.StringVar()
    total_var = tk.StringVar()
    iva_entry = tk.Entry(frame, textvariable=iva_var)
    iva_entry.grid(row=5, column=7, padx=5, pady=5)
    iva_entry.bind(
        "<KeyRelease>",
        lambda e: actualizar_subtotal(entradas, subtotal_var, iva_var, total_var),
    )

    tk.Label(frame, text="Subtotal =").grid(row=4, column=6, padx=5, pady=5, sticky="e")
    tk.Label(frame, textvariable=subtotal_var).grid(
        row=4, column=7, padx=5, pady=5, sticky="w"
    )
    tk.Label(frame, text="IVA =").grid(row=5, column=6, padx=5, pady=5, sticky="e")
    tk.Label(frame, text="Total =").grid(row=6, column=6, padx=5, pady=5, sticky="e")
    tk.Label(frame, textvariable=total_var).grid(
        row=6, column=7, padx=5, pady=5, sticky="w"
    )

    for campo in ["Cantidad", "Precio", "% Descuento"]:
        entradas[campo].bind(
            "<KeyRelease>",
            lambda e: actualizar_subtotal(entradas, subtotal_var, iva_var, total_var),
        )

    tk.Button(
        frame,
        text="Guardar",
        bg="red",
        fg="white",
        command=lambda: guardar_presupuesto(
            entradas, capitulos, subtotal_var, iva_var, total_var
        ),
    ).grid(row=7, column=2, columnspan=2, pady=10)


def mostrar_detalles(nombre_presupuesto):
    nombre_presupuesto = nombre_presupuesto.split(" - ")[0]  # Extraemos el nombre
    print(nombre_presupuesto)

    conn = sqlite3.connect("presupuestos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM presupuestos WHERE nombre = ?", (nombre_presupuesto,))
    presupuesto = cursor.fetchone()
    print(presupuesto)
    conn.close()

    if not presupuesto:
        messagebox.showerror("Error", "No se encontró el presupuesto")
        return

    ventana_detalles = tk.Toplevel()
    ventana_detalles.title(f"Detalles - {presupuesto[1]}")
    ventana_detalles.geometry("600x400")

    campos = [
        "Nombre Porveedor",
        "Nombre",
        "Fecha",
        "Descripción",
        "Cantidad",
        "Unidad",
        "Precio",
        "% Descuento",
        "Capítulos",
        "Subtotal",
        "IVA",
        "Total",
    ]

    entries = []  # Guardamos las entradas en una lista

    for i, campo in enumerate(campos):
        tk.Label(ventana_detalles, text=campo).grid(
            row=i, column=0, padx=5, pady=5, sticky="w"
        )
        entry = tk.Entry(ventana_detalles)
        entry.grid(row=i, column=1, padx=5, pady=5)

        # Asegúrate de que el índice está correcto
        index = campos.index(campo) + 1  # El primer campo es el id, así que sumamos 1

        # Depuración: Imprimir el valor que vamos a insertar
        value_to_insert = presupuesto[index] if presupuesto[index] is not None else ""
        print(f"Insertando en {campo}: {value_to_insert}")
        entry.insert(0, value_to_insert)

        entries.append(entry)  # Guardamos la referencia a los entries

    # Cambiar todos los entries a readonly después de llenar los datos
    for entry in entries:
        entry.config(state="readonly")

    tk.Button(ventana_detalles, text="Cerrar", command=ventana_detalles.destroy).grid(
        row=len(campos), column=0, columnspan=2, pady=10
    )


def ver_presupuestos():
    ventana_lista = tk.Toplevel()
    ventana_lista.title("Presupuestos Guardados")
    ventana_lista.geometry("600x500")

    tk.Label(ventana_lista, text="Buscar por Nombre o Fecha:").pack(pady=5)
    search_entry = tk.Entry(ventana_lista)
    search_entry.pack(pady=5)

    listbox = tk.Listbox(ventana_lista, width=80, height=15)
    listbox.pack(pady=10)

    btn_ver_detalles = tk.Button(
        ventana_lista,
        text="Ver Detalles",
        bg="red",
        fg="white",
        state=tk.DISABLED,
        command=lambda: mostrar_detalles(listbox.get(listbox.curselection()[0])),
    )
    btn_ver_detalles.pack(pady=5)

    def cargar_presupuestos():
        listbox.delete(0, tk.END)
        query = search_entry.get()
        conn = sqlite3.connect("presupuestos.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT nombre, fecha FROM presupuestos WHERE nombre LIKE ? OR fecha LIKE ?",
            (f"%{query}%", f"%{query}%"),
        )
        for row in cursor.fetchall():
            listbox.insert(tk.END, f"{row[0]} - {row[1]}")
        conn.close()

    def on_select(event):
        seleccion = listbox.curselection()
        if seleccion:
            btn_ver_detalles.config(
                state=tk.NORMAL
            )  # Habilita el botón si hay selección
        else:
            btn_ver_detalles.config(
                state=tk.DISABLED
            )  # Deshabilita el botón si no hay selección

    listbox.bind("<<ListboxSelect>>", on_select)

    search_entry.bind("<KeyRelease>", lambda e: cargar_presupuestos())
    cargar_presupuestos()


root = tk.Tk()
root.title("Administrativo")
root.geometry("300x200")

tk.Button(root, text="Crear Presupuesto", command=crear_presupuesto).pack(pady=10)
tk.Button(root, text="Presupuestos", command=ver_presupuestos).pack(pady=10)
tk.Button(root, text="Cargar Factura", command=lambda: print("Función pendiente")).pack(
    pady=10
)

root.mainloop()
