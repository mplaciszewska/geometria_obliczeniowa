import tkinter


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def det_function(a, b, p):
    return (a.x * b.y) + (b.x * p.y) + (p.x * a.y) - ((p.x * b.y) + (a.x * p.y) + (b.x * a.y))


def vect_function(a, b, p):
    return (b.x - a.x) * (p.y - a.y) - (p.x - a.x) * (b.y - a.y)

def difference_function (a, b, p):
    return ((a.x * b.y) + (b.x * p.y) + (p.x * a.y) - ((p.x * b.y) + (a.x * p.y) + (b.x * a.y))) - ((b.x - a.x) * (p.y - a.y) - (p.x - a.x) * (b.y - a.y))


def result():
    try:
        ax = float(ax_entry.get())
        ay = float(ay_entry.get())
        bx = float(bx_entry.get())
        by = float(by_entry.get())
        px = float(px_entry.get())
        py = float(py_entry.get())

        a = Point(ax, ay)
        b = Point(bx, by)
        p = Point(px, py)

        det = det_function(a, b, p)
        vect = vect_function(a, b, p)
        difference = difference_function (a, b, p)

        result_label.config(
            text=f"Wyznacznik: {det:.16f}, Iloczyn wektorowy: {vect:.16f}, Różnica: {difference:.16f}")

        if det > 0:
            answer_label.config(
                text="Punkt P znajduje się po prawej stronie odcinka AB")
        elif det < 0:
            answer_label.config(
                text="Punkt P znajduje się po lewej stronie odcinka AB")
        else:
            answer_label.config(text="Punkt P znajduje się na odcinku AB")
    except ValueError:
        result_label.config(text="Wprowadzono nieprawidłową wartość.")


root = tkinter.Tk()
root.title("Wyznaczanie po której stronie odcinka leży punkt")


# labele, pola tekstowe i przyciski w oknie graficznym
a_label = tkinter.Label(root, text="Podaj współrzędne punktu A:")
b_label = tkinter.Label(root, text="Podaj współrzędne punktu B:")
p_label = tkinter.Label(root, text="Podaj współrzędne punktu P:")
ax = tkinter.Label(root, text="x:")
ay = tkinter.Label(root, text="y:")
bx = tkinter.Label(root, text="x:")
by = tkinter.Label(root, text="y:")
px = tkinter.Label(root, text="x:")
py = tkinter.Label(root, text="y:")

bx = tkinter.Label(root, text="B(x):")
by = tkinter.Label(root, text="B(y):")
cx = tkinter.Label(root, text="C(x):")
cy = tkinter.Label(root, text="C(y):")

calculate_button = tkinter.Button(root, text="Oblicz", command=result)
result_label = tkinter.Label(root, text="")
answer_label = tkinter.Label(root, text="")

a_label.grid(row=0, column=0, columnspan=2)
ax.grid(row=1, column=0)
ax_entry.grid(row=1, column=1)
ay.grid(row=1, column=2)
ay_entry.grid(row=1, column=3)
b_label.grid(row=2, column=0, columnspan=2)
bx.grid(row=3, column=0)
bx_entry.grid(row=3, column=1)
by.grid(row=3, column=2)
by_entry.grid(row=3, column=3)
p_label.grid(row=4, column=0, columnspan=2)
px.grid(row=5, column=0)
px_entry.grid(row=5, column=1)
py.grid(row=5, column=2)
py_entry.grid(row=5, column=3)

calculate_button.grid(row=6, column=0, columnspan=4)
result_label.grid(row=7, column=0, columnspan=4)
answer_label.grid(row=8, column=0, columnspan=4)


root.mainloop()
