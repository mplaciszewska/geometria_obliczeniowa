import tkinter
from tkinter import Canvas
from tkinter import ttk
from tkinter import colorchooser
from tkinter import filedialog


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


line_thickness_1 = 1
line_thickness_2 = 1
line_color_1 = "blue"
line_color_2 = "blue"
line_style_1 = ()
line_style_2 = ()


def intersection(a, b, c, d):
    denominator = (b.x - a.x) * (d.y - c.y) - (b.y - a.y) * (d.x - c.x)

    if denominator == 0:
        # Lines are parallel and may not intersect.
        return None

    t1 = ((c.x - a.x) * (d.y - c.y) - (c.y - a.y) * (d.x - c.x)) / denominator
    t2 = ((c.x - a.x) * (b.y - a.y) - (c.y - a.y) * (b.x - a.x)) / denominator

    if 0 <= t1 <= 1 and 0 <= t2 <= 1:
        p = Point(a.x + t1 * (b.x - a.x), a.y + t1 * (b.y - a.y))
        return p
    return None


def open_data_from_file():
    file_path = filedialog.askopenfilename(title="Wczytaj dane z pliku")
    if file_path:
        with open(file_path, 'r') as file:
            # Odczytaj całą linię z pliku
            line = file.readline()
            # Podziel linię na współrzędne x i y, oddzielone spacją
            coordinates = line.strip().split()
            if len(coordinates) != 8:
                raise ValueError("Nieprawidłowy format danych w pliku")
            ax, ay, bx, by, cx, cy, dx, dy = map(float, coordinates)
            ax_entry.delete(0, "end")
            ax_entry.insert(0, ax)
            ay_entry.delete(0, "end")
            ay_entry.insert(0, ay)
            bx_entry.delete(0, "end")
            bx_entry.insert(0, bx)
            by_entry.delete(0, "end")
            by_entry.insert(0, by)
            cx_entry.delete(0, "end")
            cx_entry.insert(0, cx)
            cy_entry.delete(0, "end")
            cy_entry.insert(0, cy)
            dx_entry.delete(0, "end")
            dx_entry.insert(0, dx)
            dy_entry.delete(0, "end")
            dy_entry.insert(0, dy)


def save_data_to_file():
    file_path = filedialog.asksaveasfilename(
        title="Wybierz miejsce zapisu pliku")
    if file_path:
        with open(file_path, 'w') as file:
            ax = float(ax_entry.get())
            ay = float(ay_entry.get())
            bx = float(bx_entry.get())
            by = float(by_entry.get())
            cx = float(cx_entry.get())
            cy = float(cy_entry.get())
            dx = float(dx_entry.get())
            dy = float(dy_entry.get())

            a = Point(ax, ay)
            b = Point(bx, by)
            c = Point(cx, cy)
            d = Point(dx, dy)

            intersect = intersection(a, b, c, d)
            file.write(f"{intersect.x} {intersect.y}\n")


def calculate_intersection():
    try:
        ax = float(ax_entry.get())
        ay = float(ay_entry.get())
        bx = float(bx_entry.get())
        by = float(by_entry.get())
        cx = float(cx_entry.get())
        cy = float(cy_entry.get())
        dx = float(dx_entry.get())
        dy = float(dy_entry.get())

        a = Point(ax, ay)
        b = Point(bx, by)
        c = Point(cx, cy)
        d = Point(dx, dy)

        intersect = intersection(a, b, c, d)

        if intersect is not None:
            p_label_x.config(text="P(x): {}".format(intersect.x))
            p_label_y.config(text="P(y): {}".format(intersect.y))

            # Clear the canvas
            canvas.delete("all")

            # Calculate scaling factors
            xmin = min(ax, bx, cx, dx)
            ymin = min(ay, by, cy, dy)
            xmax = max(ax, bx, cx, dx)
            ymax = max(ay, by, cy, dy)
            sx = 500 / (ymax - ymin)
            sy = 300 / (xmax - xmin)

            # Obliczenie marginesu od granicy obszaru
            margin = 20  # Margines od granicy obszaru

            # Obliczenia współrzędnych z uwzględnieniem marginesu
            ax_scaled = round(margin + sx * (ay - ymin))
            ay_scaled = round(400 - margin - sy * (ax - xmin))
            bx_scaled = round(margin + sx * (by - ymin))
            by_scaled = round(400 - margin - sy * (bx - xmin))
            cx_scaled = round(margin + sx * (cy - ymin))
            cy_scaled = round(400 - margin - sy * (cx - xmin))
            dx_scaled = round(margin + sx * (dy - ymin))
            dy_scaled = round(400 - margin - sy * (dx - xmin))
            px_scaled = round(margin + sx * (intersect.y - ymin))
            py_scaled = round(400 - margin - sy * (intersect.x - xmin))

            # Rysuj punkty A, B, C, D i P na rysunku z podpisami
            canvas.create_oval(ax_scaled - 3, ay_scaled - 3,
                               ax_scaled + 3, ay_scaled + 3)
            canvas.create_text(ax_scaled, ay_scaled - 10,
                               text="A", tags=("text"))
            canvas.create_oval(bx_scaled - 3, by_scaled - 3,
                               bx_scaled + 3, by_scaled + 3)
            canvas.create_text(bx_scaled, by_scaled - 10,
                               text="B", tags=("text"))
            canvas.create_oval(cx_scaled - 3, cy_scaled - 3,
                               cx_scaled + 3, cy_scaled + 3)
            canvas.create_text(cx_scaled, cy_scaled - 10,
                               text="C", tags=("text"))
            canvas.create_oval(dx_scaled - 3, dy_scaled - 3,
                               dx_scaled + 3, dy_scaled + 3)
            canvas.create_text(dx_scaled, dy_scaled - 10,
                               text="D", tags=("text"))
            canvas.create_oval(px_scaled - 3, py_scaled - 3,
                               px_scaled + 3, py_scaled + 3)
            canvas.create_text(px_scaled, py_scaled - 10,
                               text="P", tags=("text"))

            # Draw lines AB and CD
            canvas.create_line(ax_scaled, ay_scaled, bx_scaled, by_scaled, fill=line_color_1,
                               width=line_thickness_1, dash=line_style_1, tags=("lines"))
            canvas.create_line(cx_scaled, cy_scaled, dx_scaled, dy_scaled, fill=line_color_2,
                               width=line_thickness_2, dash=line_style_2, tags=("lines"))
        else:
            p_label_x.config(text="P(x): N/A")
            p_label_y.config(text="P(y): N/A")

    except ValueError:
        p_label_x.config(text="P(x): ")
        p_label_y.config(text="P(y): ")


root = tkinter.Tk()
root.title("Wyznaczanie punktu przecięcia dwóch odcinków")


ax_label = tkinter.Label(root, text="A(x):")
ax_entry = tkinter.Entry(root)
ay_label = tkinter.Label(root, text="A(y):")
ay_entry = tkinter.Entry(root)
bx_label = tkinter.Label(root, text="B(x):")
bx_entry = tkinter.Entry(root)
by_label = tkinter.Label(root, text="B(y):")
by_entry = tkinter.Entry(root)
cx_label = tkinter.Label(root, text="C(x):")
cx_entry = tkinter.Entry(root)
cy_label = tkinter.Label(root, text="C(y):")
cy_entry = tkinter.Entry(root)
dx_label = tkinter.Label(root, text="D(x):")
dx_entry = tkinter.Entry(root)
dy_label = tkinter.Label(root, text="D(y):")
dy_entry = tkinter.Entry(root)
p_label_x = tkinter.Label(root, text="P(x):")
p_label_y = tkinter.Label(root, text="P(y):")


# Rozmieszczenie elementów na interfejsie
ax_label.grid(row=0, column=0, pady=7)
ax_entry.grid(row=0, column=1)
ay_label.grid(row=0, column=2, pady=7)
ay_entry.grid(row=0, column=3)
bx_label.grid(row=1, column=0, pady=7)
bx_entry.grid(row=1, column=1)
by_label.grid(row=1, column=2, pady=7)
by_entry.grid(row=1, column=3)
cx_label.grid(row=2, column=0, pady=7)
cx_entry.grid(row=2, column=1)
cy_label.grid(row=2, column=2, pady=7)
cy_entry.grid(row=2, column=3)
dx_label.grid(row=3, column=0, pady=7)
dx_entry.grid(row=3, column=1)
dy_label.grid(row=3, column=2, pady=7)
dy_entry.grid(row=3, column=3)
p_label_x.grid(row=4, column=2, columnspan=2)
p_label_y.grid(row=5, column=2,  columnspan=2)

canvas = tkinter.Canvas(root, width=700, height=400, bg="white")
canvas.grid(row=0, column=4, columnspan=15, rowspan=20, pady=7, padx=5)

# Tworzenie przycisku do obliczeń
calculate_button = tkinter.Button(
    root, text="Oblicz", command=calculate_intersection)
calculate_button.grid(row=4, column=0, columnspan=2,  pady=7, ipadx=20)


def update_line_thickness_1(event):
    canvas.delete("lines")
    global line_thickness_1
    new_thickness_1 = int(line_thickness_var_1.get())
    line_thickness_1 = new_thickness_1
    calculate_intersection()  # Aktualizuj grubość linii po zmianie'


 # Przyciski do zmiany grubości linii (Combobox)
line_thickness_label_1 = tkinter.Label(root, text="Grubość linii:")
line_thickness_var_1 = tkinter.StringVar()
line_thickness_var_1.set(1)
line_thickness_combo_1 = ttk.Combobox(
    root, textvariable=line_thickness_var_1, values=[1, 2, 3, 4, 5], width=15)
line_thickness_label_1.grid(row=21, column=4, pady=4)
line_thickness_combo_1.grid(row=21, column=5, columnspan=1, pady=4)
line_thickness_combo_1.bind("<<ComboboxSelected>>", update_line_thickness_1)


def update_line_thickness_2(event):
    canvas.delete("lines")
    global line_thickness_2
    new_thickness_2 = int(line_thickness_var_2.get())
    line_thickness_2 = new_thickness_2
    calculate_intersection()  # Aktualizuj grubość linii po zmianie'


 # Przyciski do zmiany grubości linii (Combobox)
line_thickness_label_2 = tkinter.Label(root, text="Grubość linii:")
line_thickness_var_2 = tkinter.StringVar()
line_thickness_var_2.set(1)
line_thickness_label_2.grid(row=21, column=4, pady=4)
line_thickness_combo_2 = ttk.Combobox(
    root, textvariable=line_thickness_var_2, values=[1, 2, 3, 4, 5], width=15)
line_thickness_combo_2.grid(row=22, column=5, columnspan=1, pady=4)
line_thickness_combo_2.bind("<<ComboboxSelected>>", update_line_thickness_2)


# zmiana koloru linii
line_color_label = tkinter.Label(root, text="Kolor linii:")
line_color_label.grid(row=23, column=4, pady=4)


def choose_line_color_1():
    canvas.delete("lines")
    global line_color_1
    color = colorchooser.askcolor(
        title="Wybierz kolor linii", color=line_color_1)
    if color[1]:
        line_color_1 = color[1]
        calculate_intersection()  # Aktualizuj kolor linii po zmianie


def choose_line_color_2():
    canvas.delete("lines")
    global line_color_2
    color = colorchooser.askcolor(
        title="Wybierz kolor linii", color=line_color_2)
    if color[1]:
        line_color_2 = color[1]
        calculate_intersection()  # Aktualizuj kolor linii po zmianie


points_visibility_label = tkinter.Label(
    root, text="Widoczność oznaczeń punktów:")
points_visibility_label.grid(row=8, column=0, pady=2, columnspan=2, padx=10)

# funkcja ukrywania etykiet punktow


def hide_points():
    canvas.delete("text")


hide_points_button = tkinter.Button(
    root, text="Ukryj", command=hide_points)
hide_points_button.grid(row=8, column=2, rowspan=1,
                        ipadx=32, padx=10, columnspan=2)


def show_points():
    canvas.delete("all")
    calculate_intersection()


show_points_button = tkinter.Button(
    root, text="Pokaż", command=show_points)
show_points_button.grid(row=9, column=2, rowspan=1,
                        ipadx=30, padx=10, columnspan=2)

# Dodaj przycisk do wyboru koloru linii
color_button_1 = tkinter.Button(
    root, text="Wybierz kolor linii 1", command=choose_line_color_1)
color_button_1.grid(row=23, column=5, pady=4)

color_button_2 = tkinter.Button(
    root, text="Wybierz kolor linii 2", command=choose_line_color_2)
color_button_2.grid(row=23, column=6, pady=4, padx=5)

# Przycisk do wczytywania danych z pliku
load_data_button = tkinter.Button(
    root, text="Wczytaj dane z pliku", command=open_data_from_file)
load_data_button.grid(row=6, column=0, columnspan=2, padx=10, ipadx=10)

save_data_button = tkinter.Button(
    root, text="Zapisz wyniki do pliku", command=save_data_to_file)
save_data_button.grid(row=6, column=2, columnspan=2, ipadx=10)


def set_line_style_1_solid():

    global line_style_1
    line_style_1 = ()
    calculate_intersection()


def set_line_style_1_dotted():

    global line_style_1
    line_style_1 = (1,)
    calculate_intersection()


def set_line_style_2_solid():

    global line_style_2
    line_style_2 = ()
    calculate_intersection()


def set_line_style_2_dotted():

    global line_style_2
    line_style_2 = (1,)
    calculate_intersection()


line_style_label_1 = tkinter.Label(root, text="Styl linii 1:")
line_style_solid_button_1 = tkinter.Button(
    root, text="Solid", command=set_line_style_1_solid)
line_style_dotted_button_1 = tkinter.Button(
    root, text="Dotted", command=set_line_style_1_dotted)
line_style_label_1.grid(row=21, column=8, pady=4)
line_style_solid_button_1.grid(row=21, column=9, pady=4, ipadx=12)
line_style_dotted_button_1.grid(row=21, column=10, pady=4, ipadx=10)

line_style_label_2 = tkinter.Label(root, text="Styl linii 2:")
line_style_solid_button_2 = tkinter.Button(
    root, text="Solid", command=set_line_style_2_solid)
line_style_dotted_button_2 = tkinter.Button(
    root, text="Dotted", command=set_line_style_2_dotted)
line_style_label_2.grid(row=22, column=8, pady=4)
line_style_solid_button_2.grid(row=22, column=9, pady=4, ipadx=12)
line_style_dotted_button_2.grid(row=22, column=10, pady=4, ipadx=10)


root.mainloop()
