import tkinter as tk
from tkinter import filedialog, Entry, Button
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import colorchooser
from tkinter import ttk

global_points = []
bounding_rect_artist = None
convex_hull_artist = None
current_rect_linestyle = '-'
current_hull_linestyle = '-'

def draw_axes(ax):
    # Usuń oznaczenia osi i indeksy
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('none') 
    ax.yaxis.set_ticks_position('none')

def create_empty_plot():
    fig, ax = plt.subplots(figsize=(9, 9))
    draw_axes(ax)
    plot_title = fig.suptitle("WYKRES", y=0.95, fontsize=16, fontweight='bold')
    return fig, ax, plot_title

def read_points_from_file(file_path_2):
    with open(file_path_2, 'r') as file:
        lines = file.readlines()
        points = [tuple(map(float, line.strip().split())) for line in lines]
    return points

def draw_points(ax, points):
    if points:
        y, x = zip(*points)  # Zamiana x i y
        ax.scatter(x, y, color=current_point_color, marker='o', s=current_point_size)
    
def draw_bounding_rectangle(ax, points):
    global bounding_rect_artist, current_rect_color, current_rect_thickness, current_rect_linestyle
    # Usuń poprzedni prostokąt, jeśli istnieje
    if bounding_rect_artist is not None:
        bounding_rect_artist.remove()

    if points:
        min_x = min(p[1] for p in points)
        min_y = min(p[0] for p in points)
        max_x = max(p[1] for p in points)
        max_y = max(p[0] for p in points)

        # Utwórz nowego artystę prostokąta
        rect = plt.Rectangle((min_x, min_y), max_x - min_x, max_y - min_y, edgecolor=current_rect_color, facecolor='none', 
                             linewidth=current_rect_thickness,  linestyle=current_rect_linestyle)
        ax.add_patch(rect)
        bounding_rect_artist = rect

    canvas.draw()

def remove_bounding_rectangle():
    global bounding_rect_artist
    # Usuń poprzedni prostokąt
    if bounding_rect_artist is not None:
        bounding_rect_artist.remove()
        bounding_rect_artist = None
        canvas.draw()

def jarvis_algorithm(Q):
    n = len(Q)
    if n < 3:
        return None
    result = []  
    P0 = find_leftmost_point(Q)
    result.append(P0)
    while True:
        Q_next = None
        for P in Q:
            if P == result[-1]:
                continue
            if Q_next is None or orientation(result[-1], P, Q_next) == "right":
                Q_next = P
        if Q_next == P0:
            break 
        result.append(Q_next)
    return result

def find_leftmost_point(Q):
    P0 = Q[0]
    for P in Q:
        if P[0] < P0[0] or (P[0] == P0[0] and P[1] < P0[1]):
            P0 = P
    return P0

def orientation(P1, P2, P3):
    val = (P2[1] - P1[1]) * (P3[0] - P2[0]) - (P2[0] - P1[0]) * (P3[1] - P2[1])

    if val == 0:
        return "collinear"
    elif val > 0:
        return "left"
    else:
        return "right"

def draw_convex_hull(ax):
    global global_points, convex_hull_artist, current_ch_thickness, current_hull_linestyle
    convex_hull_points = jarvis_algorithm(global_points)
    if convex_hull_points:
        y, x = zip(*convex_hull_points)
        convex_hull_artist = ax.plot(x + (x[0],), y + (y[0],), color=current_ch_color, linewidth=current_ch_thickness, linestyle=current_hull_linestyle)
    else:
        print("Nie można utworzyć otoczki wypukłej. Za mało punktów.")

    canvas.draw()

def remove_convex_hull():
    global convex_hull_artist
    if convex_hull_artist is not None:
        for artist in convex_hull_artist:
            artist.remove()
        convex_hull_artist = None
        canvas.draw()
    

def save_convex_hull_to_file():
    global global_points
    convex_hull_points = jarvis_algorithm(global_points)
    if convex_hull_points:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        with open(file_path, 'w') as file:
            for point in convex_hull_points:
                file.write(f"{point[0]} {point[1]}\n")
        print(f"Zapisano punkty z otoczki wypukłej do pliku: {file_path}")
    else:
        print("Nie można utworzyć otoczki wypukłej. Za mało punktów.")


def draw_points_from_file(ax, file_path):
    global global_points, bounding_rect_artist, convex_hull_artist
    for artist in ax.collections:
        artist.remove()
    if convex_hull_artist is not None:
        for artist in convex_hull_artist:
            artist.remove()
            
    if ax.texts:
            hide_numbers(ax)
    points = read_points_from_file(file_path)
    global_points = points 
    draw_bounding_rectangle(ax, points)
    draw_points(ax, points)
    add_point_numbers(ax, global_points)

    if points:
        min_x = min(p[1] for p in points) 
        min_y = min(p[0] for p in points) 
        max_x = max(p[1] for p in points) 
        max_y = max(p[0] for p in points) 

        ax.spines['left'].set_position(('data', min_x))
        ax.spines['bottom'].set_position(('data', min_y))
        ax.set_xlim(left=min_x - 2, right=max_x + 2)
        ax.set_ylim(bottom=min_y - 2, top=max_y + 2)

    canvas.draw()

def add_point_entry(entry_x, entry_y, ax):
    global global_points, bounding_rect_artist, convex_hull_artist
    try:
        x = float(entry_y.get())
        y = float(entry_x.get())
        if ax.texts:
            hide_numbers(ax)
        global_points.append((x, y))
        if bounding_rect_artist is not None:
            bounding_rect_artist.remove()
            bounding_rect_artist = None
        if convex_hull_artist is not None:
            for artist in convex_hull_artist:
                artist.remove()
            convex_hull_artist = None
        draw_bounding_rectangle(ax, global_points)
        draw_points(ax, global_points)
        add_point_numbers(ax, global_points)
        min_x = min(p[1] for p in global_points) - 2
        min_y = min(p[0] for p in global_points) - 2
        max_x = max(p[1] for p in global_points) + 2
        max_y = max(p[0] for p in global_points) + 2
        ax.set_xlim(left=min_x, right=max_x)
        ax.set_ylim(bottom=min_y, top=max_y)
        entry_x.delete(0, tk.END)
        entry_y.delete(0, tk.END)
    except ValueError:
        print("Błędny format punktu. Podaj dwie współrzędne liczbowe.")

    canvas.draw()


# FUNKCJE DO EDYCJI KOLORÓW I STYLÓW
current_point_color = 'blue'
current_ch_color = 'gray'
current_rect_color = 'gray'
current_point_size = 20
current_ch_thickness = 2.0
current_rect_thickness = 2.0

def change_points_color(ax, point_color_label):
    global current_point_color
    color = colorchooser.askcolor()[1] 
    current_point_color = color
    for collection in ax.collections:
        collection.set_color(color)
    canvas.draw()
    point_color_label.configure(bg=current_point_color)

def change_points_size(ax, point_size_entry):
    global current_point_size
    try:
        current_point_size = float(point_size_entry.get())
        for collection in ax.collections:
            collection.set_sizes([current_point_size])
        canvas.draw()
    except ValueError:
        print("Błędny format grubości punktów. Podaj liczbę.")

def add_point_numbers(ax, points):
    for i, point in enumerate(points):
        ax.annotate(str(i + 1), (point[1], point[0]), textcoords="offset points", xytext=(0, 5), ha='center')
    canvas.draw()

def hide_numbers(ax):
    global canvas
    for text in ax.texts:
        text.remove()
    canvas.draw()

def toggle_numbers(ax, show_numbers_var):
    global canvas
    for text in ax.texts:
        text.set_visible(show_numbers_var.get())
    canvas.draw()

def change_convex_hull_color(ax, ch_color_label):
    global convex_hull_artist, current_ch_color
    if convex_hull_artist is not None:
        color = colorchooser.askcolor()[1]
        current_ch_color = color
        for line in convex_hull_artist:
            line.set_color(color)
        canvas.draw()
    ch_color_label.configure(bg=current_ch_color)

def change_rect_color(ax, rect_color_label):
    global current_rect_color, bounding_rect_artist
    color = colorchooser.askcolor()[1]
    current_rect_color = color
    if bounding_rect_artist is not None:
        bounding_rect_artist.set_edgecolor(color)
    canvas.draw()
    rect_color_label.configure(bg=current_rect_color)

def change_ch_thickness(ax, ch_thickness_entry):
    global current_ch_thickness
    try:
        current_ch_thickness = float(ch_thickness_entry.get())
        if convex_hull_artist is not None:
            for line in convex_hull_artist:
                line.set_linewidth(current_ch_thickness)
            canvas.draw()
    except ValueError:
        print("Błędny format grubości otoczki. Podaj liczbę.")

def change_rect_thickness(ax, rect_thickness_entry):
    global current_rect_thickness
    try:
        current_rect_thickness = float(rect_thickness_entry.get())
        if bounding_rect_artist is not None:
            bounding_rect_artist.set_linewidth(current_rect_thickness)
            canvas.draw()
    except ValueError:
        print("Błędny format grubości prostokąta. Podaj liczbę.")

def change_rect_linestyle(ax, linestyle_var):
    global current_rect_linestyle
    current_rect_linestyle = linestyle_var.get()
    if bounding_rect_artist is not None:
        bounding_rect_artist.set_linestyle(current_rect_linestyle)
        canvas.draw()

def change_hull_linestyle(ax, linestyle_var):
    global current_hull_linestyle
    current_hull_linestyle = linestyle_var.get()
    if convex_hull_artist is not None:
        for line in convex_hull_artist:
            line.set_linestyle(current_hull_linestyle)
        canvas.draw()

def main():
    global canvas, save_convex_hull_button
    root = tk.Tk()
    root.title("WYZNACZENIE OTOCZKI WYPUKŁEJ ZBIORU PUNKTÓW")
    font_style = ("Helvetica", 16)
    font_style_bold = ("Helvetica", 16, "bold")

    # Ramka do przechowywania wykresu
    plot_frame = tk.Frame(root)
    plot_frame.grid(row=0, column=0, sticky='nw', rowspan=30, padx=10, pady=20)
    fig, ax, plot_title = create_empty_plot()

    # dodawanie punktow
    read_points_label = tk.Label(root, text = "--------------  Dodawanie punktów  --------------",  font=font_style_bold, bg='lightgray')
    read_points_label.grid(row = 0, column = 1, columnspan=4, padx = 10, pady = (12, 0), ipady = 6)

    read_button = tk.Button(root, text="Wczytaj punkty z pliku", font=font_style, width = 35, command=lambda: draw_points_from_file(ax, filedialog.askopenfilename(
                                       title="Wybierz plik z punktami",
                                       filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
                                   )))
    read_button.grid(row=1, column=1, columnspan = 4, sticky='w', padx=10, pady=(0, 10))

    label_x = tk.Label(root, text="X:", font=font_style)
    label_x.grid(row=2, column=1, sticky='w', padx=10, pady=0)
    entry_x = Entry(root, font=font_style,  width = 15)
    entry_x.grid(row=2, column=2, sticky='w', padx=0, pady=0)

    label_y = tk.Label(root, text="Y:", font=font_style)
    label_y.grid(row=3, column=1, sticky='w', padx=10, pady=0)
    entry_y = Entry(root, font=font_style, width = 15)
    entry_y.grid(row=3, column=2, sticky='w', padx=0, pady=0)

    add_point_button = Button(root, text="Dodaj punkt", font=font_style, width= 15, command=lambda: add_point_entry(entry_x, entry_y, ax))
    add_point_button.grid(row=2, column=3, columnspan = 2, rowspan = 2, padx=10, pady=10)

    point_color_label = tk.Label(root, text="",  bg='white', relief=tk.SOLID, font=font_style, width = 2)
    point_color_label.grid(row=4, column=3, sticky='w', pady=10)

    color_button = tk.Button(root, text="Zmień kolor punktów", font=font_style, width=17,
                         command=lambda: change_points_color(ax, point_color_label))
    color_button.grid(row=4, column=1, columnspan=2, sticky='w', padx=10, pady=10)

    point_size_entry = Entry(root, font=font_style, width=15)
    point_size_entry.grid(row=5, column=3,columnspan = 2, sticky='w', padx=0, pady=0)

    label_size = tk.Label(root, text="Grubość punktów:", font=font_style)
    label_size.grid(row=5, column=1, columnspan = 2, sticky='w', padx=10, pady=0)

    point_size_entry.bind("<KeyRelease>", lambda event: change_points_size(ax, point_size_entry))

    show_numbers_var = tk.BooleanVar()
    show_numbers_var.set(True)  # Domyślnie pokazuj numery

    toggle_numbers_button = tk.Checkbutton(root, text="Numeracja", font=font_style, variable=show_numbers_var,
                                           command=lambda: toggle_numbers(ax, show_numbers_var))
    toggle_numbers_button.grid(row=4, column=4, sticky='w', padx=(0,0), pady=10)


    # otoczka wypukla
    draw_ch_label = tk.Label(root, text = "---------  Budowanie otoczki wypukłej  --------", font=font_style_bold, bg='lightgray')
    draw_ch_label.grid(row = 7, column = 1, columnspan = 4, padx =10, pady =(10,0), ipady = 6)

    draw_convex_hull_button = tk.Button(root, text="Zbuduj Otoczkę", font=font_style, width = 17,
                                        command=lambda: draw_convex_hull(ax))
    draw_convex_hull_button.grid(row=8, column=1, columnspan=2, sticky='w', padx=(10, 0), pady=7)

    remove_convex_hull_button = tk.Button(root, text="Usuń Otoczkę", font=font_style, width = 17,
                                          command=remove_convex_hull)
    remove_convex_hull_button.grid(row=8, column=3, columnspan=2, sticky='w', padx=(0, 10), pady=7)

    save_convex_hull_button = tk.Button(root, text="Zapisz Otoczkę", font=font_style, width = 36,
                                        command=save_convex_hull_to_file)
    save_convex_hull_button.grid(row=9, column=1, columnspan=4, sticky='w', padx=10, pady=7)

    color_convex_hull_button = tk.Button(root, text="Zmień kolor otoczki", font=font_style, width=17,
                                     command=lambda: change_convex_hull_color(ax, ch_color_label))
    color_convex_hull_button.grid(row=10, column=1, columnspan=2, sticky='w', padx=(10, 0), pady=7)

    ch_color_label = tk.Label(root, text="",  bg='white', relief=tk.SOLID, font=font_style, width = 2)
    ch_color_label.grid(row=10, column=3, sticky='w', pady=7)

    ch_thickness_entry = Entry(root, font=font_style, width=15)
    ch_thickness_entry.grid(row=11, column=3, columnspan=2, sticky='w', padx=0, pady=0)

    label_ch_thickness = tk.Label(root, text="Grubość otoczki:", font=font_style)
    label_ch_thickness.grid(row=11, column=1, columnspan=2, sticky='w', padx=10, pady=0)

    ch_thickness_entry.bind("<KeyRelease>", lambda event: change_ch_thickness(ax, ch_thickness_entry))

    linestyle_ch_combobox = ttk.Combobox(root, font=font_style, values=['-', '--', '-.', ':'], width=12)
    linestyle_ch_combobox.set(current_hull_linestyle)
    linestyle_ch_combobox.grid(row = 12, column = 3, columnspan = 2, pady = 0, padx = 10, sticky='w')
    label_ch_linestyle = tk.Label(root, text="Styl linii otoczki:", font=font_style)
    label_ch_linestyle.grid(row=12, column=1, columnspan=2, sticky='w', padx=9, pady=0)
    linestyle_ch_combobox.bind('<<ComboboxSelected>>', lambda event: change_hull_linestyle(ax, linestyle_ch_combobox))

    # prostokąt ograniczający
    rect_label = tk.Label(root, text = "-----------  Prostokąt ograniczający  ------------", font=font_style_bold, bg='lightgray')
    rect_label.grid(row = 13, column = 1, columnspan = 4, padx = 10, pady = (10,0), ipady = 6)
    remove_rect_button = tk.Button(root, text="Ukryj prostokąt ", font=font_style, width = 17,
                                   command=remove_bounding_rectangle)
    remove_rect_button.grid(row=14, column=1, columnspan=2, sticky='w', padx=(10, 0), pady=6)

    draw_rect_button = tk.Button(root, text="Pokaż prostokąt", font=font_style, width = 17,
                                 command=lambda: draw_bounding_rectangle(ax, global_points))
    draw_rect_button.grid(row=14, column=3, columnspan=2, sticky='w', padx=(0, 10), pady=6)

    rect_color_label = tk.Label(root, text="", bg='white', relief=tk.SOLID, font=font_style, width=2)
    rect_color_label.grid(row=15, column=3, sticky='w', pady=6)

    rect_color_button = tk.Button(root, text="zmień kolor prostokąta", font=font_style, width=17,
                                command=lambda: change_rect_color(ax, rect_color_label))
    rect_color_button.grid(row=15, column=1, columnspan=2, sticky='w', padx=(10, 0), pady=6)

    rect_thickness_entry = Entry(root, font=font_style, width=15)
    rect_thickness_entry.grid(row=16, column=3, columnspan=2, sticky='w', padx=0, pady=0)

    label_rect_thickness = tk.Label(root, text="Grubość prostokąta:", font=font_style)
    label_rect_thickness.grid(row=16, column=1, columnspan=2, sticky='w', padx=10, pady=0)

    rect_thickness_entry.bind("<KeyRelease>", lambda event: change_rect_thickness(ax, rect_thickness_entry))

    linestyle_combobox = ttk.Combobox(root, font=font_style, values=['-', '--', '-.', ':'], width=12)
    linestyle_combobox.set(current_rect_linestyle)
    linestyle_combobox.grid(row = 17, column = 3, columnspan = 2, pady = 0, padx = 10, sticky='w')
    label_linestyle = tk.Label(root, text="Styl linii prostokąta:", font=font_style)
    label_linestyle.grid(row=17, column=1, columnspan=2, sticky='w', padx=9, pady=0)
    linestyle_combobox.bind('<<ComboboxSelected>>', lambda event: change_rect_linestyle(ax, linestyle_combobox))

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    root.mainloop()

if __name__ == "__main__":
    main()
