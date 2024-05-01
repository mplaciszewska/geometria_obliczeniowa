import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from math import atan2, degrees
from tkinter import filedialog
from tkinter import colorchooser
from tkinter import ttk

def draw_axes(ax):
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.spines['left'].set_position('zero')  
    ax.spines['bottom'].set_position('zero') 
    ax.spines['right'].set_color('black')
    ax.spines['top'].set_color('black')
    ax.spines['left'].set_linewidth(1.0)
    ax.spines['bottom'].set_linewidth(1.0)
    ax.spines['right'].set_linewidth(1.0)
    ax.spines['top'].set_linewidth(1.0)
    ax.set_ylim(auto=True) 
    ax.set_ylim(auto=True)



# tworzenie układu wspolrzednych
def create_empty_plot():
    fig, ax = plt.subplots(figsize=(8, 8))
    draw_axes(ax)
    plot_title = fig.suptitle("WYKRES", y=0.95, fontsize=16, fontweight='bold')  # Dodaj tytuł do fig
    return fig, ax, plot_title

# odczytywanie wielakata
def read_polygon_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        polygon_coordinates = [tuple(map(float, line.strip().split())) for line in lines]
        polygon_coordinates.append(polygon_coordinates[0])  
    return polygon_coordinates

# odczytywanie punktów z pliku
def read_points_from_file(file_path_2):
    with open(file_path_2, 'r') as file:
        lines = file.readlines()
        points = [tuple(map(float, line.strip().split())) for line in lines]
    return points

# rysowanie
def draw_polygon(ax, polygon_coordinates):
    for line in ax.lines:
            line.remove()
    polygon_coordinates.append(polygon_coordinates[0])  
    line, = ax.plot(*zip(*polygon_coordinates), color='black', marker=None)
    line.set_label('Polygon')  # Ustawienie etykiety linii


def draw_polygon_from_file(ax, file_path):
    global polygon_coordinates
    polygon_coordinates = read_polygon_from_file(file_path)
    draw_polygon(ax, polygon_coordinates)
    # Oblicz minimalne wartości x i y z dodatkowym przesunięciem
    min_x = min(p[0] for p in polygon_coordinates) - 50
    min_y = min(p[1] for p in polygon_coordinates) - 50
    max_x = max(p[0] for p in polygon_coordinates) + 50
    max_y = max(p[1] for p in polygon_coordinates) + 50

    # Przesuń początek osi do obliczonych wartości
    ax.spines['left'].set_position(('data', min_x))
    ax.spines['bottom'].set_position(('data', min_y))
    
    # Ustaw zakres osi
    ax.set_xlim(left=min_x, right=max_x)
    ax.set_ylim(bottom=min_y, top=max_y)
    canvas.draw()

def draw_points(ax, points):
    if points:
        x, y = zip(*points)
        ax.scatter(x, y, color='blue', marker='o', s=10) 
        
def draw_points_from_file(ax, file_path_2):
    points = read_points_from_file(file_path_2)
    draw_points(ax, points)
    canvas.draw()

def draw_point(ax, x, y):
    ax.scatter(x, y, color='blue', marker='o', s=10) 

def calculate_angle_sum(point, polygon):
    angle_sum = 0
    for i in range(len(polygon)):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % len(polygon)]

        vector1 = (p1[0] - point[0], p1[1] - point[1])
        vector2 = (p2[0] - point[0], p2[1] - point[1])

        dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
        cross_product = vector1[0] * vector2[1] - vector1[1] * vector2[0]

        angle = atan2(cross_product, dot_product)
        angle_sum += angle
    angle_sum = degrees(angle_sum)
    return angle_sum

# sprawdzanie czy punkt jest wewnątrz wielokąta
def is_point_inside_polygon(point, polygon):
    angle_sum = calculate_angle_sum(point, polygon)
    return abs(angle_sum) >= 180 or is_point_on_vertex(point, polygon)

def is_point_on_vertex(point, polygon):
    for vertex in polygon[:-1]:  # Iteruj tylko do przedostatniego wierzchołka
        if point == vertex:
            return True
    return False

def change_polygon_color(ax, color_label):
    color = colorchooser.askcolor()[1]  # Wybór koloru
    for line in ax.lines:
        line.set_color(color)
    canvas.draw()
    color_label.configure(bg=color) 

def change_linestyle(ax, linestyle_var):
    linestyle = linestyle_var.get()
    for line in ax.lines:
        line.set_linestyle(linestyle)
    canvas.draw()

def change_line_width(ax, line_width_var):
    width = float(line_width_var.get())

    # Zapisz aktualną widoczność osi
    axes_visible = ax.spines['left'].get_visible(), ax.spines['right'].get_visible(), ax.spines['top'].get_visible(), ax.spines['bottom'].get_visible()

    # Ukryj osie
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # Zmiana grubości dla linii odpowiadającej wielokątowi
    for line in ax.get_lines():
        if line.get_label() == 'Polygon':
            line.set_linewidth(width)

    # Przywróć widoczność osi
    ax.spines['left'].set_visible(axes_visible[0])
    ax.spines['right'].set_visible(axes_visible[1])
    ax.spines['top'].set_visible(axes_visible[2])
    ax.spines['bottom'].set_visible(axes_visible[3])

    canvas.draw()

def main():
    global canvas
    root = tk.Tk()
    root.title("WYZNACZENIE POŁOŻENIA PUNKTU WZGLĘDEM WIELOKĄTA")
    font_style = ("Helvetica", 16)
    font_style_bold = ("Helvetica", 16, "bold")

    # Ramka do przechowywania wykresu
    plot_frame = tk.Frame(root)
    plot_frame.grid(row=0, column=0, sticky='nw', rowspan = 30, padx = 10, pady = 20)
    fig, ax, plot_title = create_empty_plot()
    
    # Płótno Tkinter z wykresem
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Ramka do rysowania wielokata
    drawing_polygon_frame = tk.Frame(root, bg='lightgrey')
    drawing_polygon_frame.grid(row=0, column=1, padx=12, pady = 16, ipady = 10)
    drawing_polygon_label = tk.Label(drawing_polygon_frame,  text = "RYSOWANIE WIELOKĄTA NA WYKRESIE", font = font_style_bold,  bg='lightgrey' )
    drawing_polygon_label.grid(row = 0, column = 0, columnspan = 2, pady = 5, padx = 30)

    # przycisk rysujący wielokąt z pliku
    draw_polygon_button = tk.Button(drawing_polygon_frame, text="Wczytaj wielokąt z pliku", font=font_style,
                                  command=lambda: draw_polygon_from_file(ax, filedialog.askopenfilename(
                                       title="Wybierz plik z wielokątem",
                                       filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
                                   )))
    draw_polygon_button.grid(row = 1, column = 0, pady = 10, sticky='w', padx = 8)

    def delete_polygon(ax):
        for line in ax.lines:
            line.remove()
        color_label.configure(bg = 'white')
        canvas.draw()
    
    delete_polygon_button = tk.Button(drawing_polygon_frame, text="Usuń wielokąt z wykresu", font=font_style,
                                   command=lambda: delete_polygon(ax))
    delete_polygon_button.grid(row=1, column=1, pady=10, sticky='e', padx = 8)

    color_label = tk.Label(drawing_polygon_frame, text="", bg='black', relief=tk.SOLID, width=3, height=2)
    color_label.grid(row=2, column=1, pady=10, sticky='w', padx=8)

    change_color_button = tk.Button(drawing_polygon_frame, text="Zmień kolor wielokąta", font=font_style,
                                command=lambda: change_polygon_color(ax, color_label))
    change_color_button.grid(row=2, column=0, pady=10, sticky='w', padx=8, ipadx = 8)

    linestyle_var = tk.StringVar(root)
    linestyle_var.set('-')  # Domyślny styl linii to ciągła linia

    # Utwórz etykietę dla stylu linii i przechowuj ją w zmiennej
    linestyle_label = ttk.Label(drawing_polygon_frame, text="    Styl linii wielokąta:", font = font_style)
    linestyle_label.grid(row=4, column=0, ipady=6, ipadx=17, padx = 8, pady = 8)

    # Utwórz rozwijaną listę dla wyboru stylu linii
    linestyle_combobox = ttk.Combobox(drawing_polygon_frame,font = font_style, textvariable=linestyle_var,
                                      values=['-', '--', '-.', ':'],  width=18)
    linestyle_combobox.grid(row=4, column=1, pady=5, padx=8)
    linestyle_combobox.bind('<<ComboboxSelected>>', lambda event: change_linestyle(ax, linestyle_var))

    line_width_var = tk.StringVar(root)
    line_width_var.set('1.0')  # Domyślna grubość linii

    line_width_label = ttk.Label(drawing_polygon_frame, text="Grubość linii wielokąta:", font=font_style)
    line_width_label.grid(row=6, column=0, pady=5, padx=8, ipadx = 6, ipady = 6)

    line_width_combobox = ttk.Combobox(drawing_polygon_frame, font=font_style, textvariable=line_width_var,
                                    values=['1.0', '2.0', '3.0', '4.0', '5.0'], width=18)
    line_width_combobox.grid(row=6, column=1, pady=5, padx=8)
    line_width_combobox.bind('<<ComboboxSelected>>', lambda event: change_line_width(ax, line_width_var))


     # Ramka do rysowania punktów
    drawing_point_frame = tk.Frame(root, bg='lightgrey')
    drawing_point_frame.grid(row=2, column=1, padx=10, pady = 10, ipadx = 11)
    drawing_point_label = tk.Label(drawing_point_frame,  text = "SPRAWDZANIE POŁOŻENIA PUNKTÓW \n WZGLĘDEM WIELOKĄTA", font = font_style_bold,  bg='lightgrey' )
    drawing_point_label.grid(row = 2, column = 0, columnspan = 2, pady = 5)

    
    # Pola do wprowadzania współrzędnych punktu
    x_entry_label = tk.Label(drawing_point_frame, text="Współrzędna x:", font=font_style, bg='lightgrey')
    x_entry_label.grid(row=3, column=0, pady = 4, padx = 5, ipady = 10)
    x_entry = tk.Entry(drawing_point_frame, font=font_style)
    x_entry.grid(row=3, column=1, pady = 4, padx = 5)

    y_entry_label = tk.Label(drawing_point_frame, text="Współrzędna y:", font=font_style, bg='lightgrey')
    y_entry_label.grid(row=4, column=0, pady = 4, padx = 5)
    y_entry = tk.Entry(drawing_point_frame, font=font_style)
    y_entry.grid(row=4, column=1, pady = 4, padx = 5)

    result_label = tk.Label(drawing_point_frame, text="", font=font_style, bg='lightgrey')
    result_label.grid(row=6, column=0, columnspan=2, pady=3)
    
    

    # rysowanie punktu 
    def draw_point_on_click(ax, x_entry_text, y_entry_text):
        # usuwanie poprzedniego punktu:
        for collection in ax.collections:
            collection.remove()
        count_points_label.config(text="")
        x = float(x_entry_text)
        y = float(y_entry_text)
        draw_point(ax, x, y)

        if is_point_inside_polygon((x, y), polygon_coordinates):
            result_label.config(text="Sprawdzany punkt znajduje się \n wewnątrz wielokąta")
        else:
            result_label.config(text="Sprawdzany punkt znajduje się \n na zewnątrz wielokąta")
        point_color_label.configure(bg='blue')
        canvas.draw()

    # Przycisk do rysowania punktu
    draw_point_button = tk.Button(drawing_point_frame, text="Sprawdź punkt", font=font_style,
                                  command=lambda: draw_point_on_click(ax, x_entry.get(), y_entry.get()))
    draw_point_button.grid(row=5, column=0, columnspan=2, pady=10)

    # rysowanie punktów wczytwanych z pliku
    def draw_points_on_click(ax, file_path_2):
        for collection in ax.collections:
            collection.remove()
        result_label.config(text = "")
        points = read_points_from_file(file_path_2)
        points_inside_polygon = [point for point in points if is_point_inside_polygon(point, polygon_coordinates)]
        draw_points(ax, points_inside_polygon)
        num_inside = len(points_inside_polygon)
        count_points_label.config(text=f"Liczba punktów wewnątrz wielokąta: {num_inside}")
        point_color_label.configure(bg='blue')
        canvas.draw()


    load_points_button = tk.Button(drawing_point_frame, text="Wczytaj punkty z pliku", font=font_style,
                                   command=lambda: draw_points_on_click(ax, filedialog.askopenfilename(
                                       title="Wybierz plik z punktami",
                                       filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
                                   )))
    load_points_button.grid(row=7, column=0, columnspan=1, pady=10, sticky='w', padx = 8, ipadx = 8)

    # wyświetlanie ile punktów jest w wielokącie
    count_points_label = tk.Label(drawing_point_frame, text="", font=font_style, bg = 'lightgrey')
    count_points_label.grid(row=8, column=0, columnspan=2, pady=10, sticky='w', padx=8)

    def change_points_color(ax, point_color_label):
        color = colorchooser.askcolor()[1]  # Wybór koloru
        for collection in ax.collections:
            collection.set_color(color)
        canvas.draw()
        point_color_label.configure(bg=color)
    

    # Przycisk do zmiany koloru punktów
    point_color_label = tk.Label(drawing_point_frame, text="", bg='white', relief=tk.SOLID, width=3, height=2)
    point_color_label.grid(row=9, column=1, pady=10, sticky='w', padx=25)

    change_points_color_button = tk.Button(drawing_point_frame, text="Zmień kolor punktów", font=font_style,
                                    command=lambda: change_points_color(ax, point_color_label))
    change_points_color_button.grid(row=9, column=0, pady=10, padx = 8, ipadx = 13)

    def change_point_size(ax, point_size_entry):
        try:
            size = float(point_size_entry.get())
            for collection in ax.collections:
                collection.set_sizes([size])
            canvas.draw()
        except ValueError:
            messagebox.showerror("Błąd", "Proszę wprowadzić prawidłową liczbę dla grubości punktów.")


    point_size_entry = tk.Entry(drawing_point_frame, font=font_style, width = 18)
    point_size_entry.grid(row=10, column=1, pady=4, padx=8, sticky = 'e')


    change_point_size_button = tk.Button(drawing_point_frame, text="Zmień grubość punktów", font=font_style,
                                     command=lambda: change_point_size(ax, point_size_entry))
    change_point_size_button.grid(row=10, column=0, pady=5, padx = 8)


    def delete_points(ax, count_points_label):
        for collection in ax.collections:
            collection.remove()
        for item in ax.lines:  
            if item.get_markerfacecolor() == 'blue':  
                item.remove()
        count_points_label.config(text="")
        result_label.config(text="")
        point_color_label.config(bg = 'white') 
        canvas.draw()

    delete_points_button = tk.Button(drawing_point_frame, text="Usuń punkty z wykresu", font=font_style,
                                 command=lambda: delete_points(ax, count_points_label))
    delete_points_button.grid(row=7, column=1, columnspan=1, pady=10, padx = 5, sticky = 'e')
    
    root.mainloop()
    
if __name__ == "__main__":
    main()
