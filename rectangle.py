from tkinter import *
from collections import deque

root = Tk()
custom_font = ("Helvetica", 24)
mylabel = Label(text="Water Jug Problem", padx=20, pady=20, font=custom_font)
mylabel.pack()
root.title("Water Jug AI")

def create_gradient_background(canvas):
    # Define gradient colors
    start_color = "#2193b0"  # Pink
    end_color = "#6dd5ed" 

    # Define the number of gradient rectangles
    num_rectangles = 100

    # Calculate the color step between each rectangle
    color_step = [(int(end_color[i:i+2], 16) - int(start_color[i:i+2], 16)) / num_rectangles for i in (1, 3, 5)]

    for i in range(num_rectangles):
        # Calculate the current color
        current_color = "#{:02X}{:02X}{:02X}".format(
            int(start_color[1:3], 16) + int(i * color_step[0]),
            int(start_color[3:5], 16) + int(i * color_step[1]),
            int(start_color[5:7], 16) + int(i * color_step[2])
        )

        # Calculate rectangle coordinates
        x0 = 0
        y0 = i * (500 / num_rectangles)
        x1 = 800
        y1 = (i + 1) * (500 / num_rectangles)

        # Draw the gradient rectangle
        canvas.create_rectangle(x0, y0, x1, y1, fill=current_color, outline="")


def create_jug(canvas, x, y, rule):
    canvas.delete("all")

    create_gradient_background(canvas)

    canvas.create_line(100, 100, 100, 350, width=3,)
    canvas.create_line(300, 100, 300, 350, width=3)
    canvas.create_line(100, 350, 300, 350, width=3)
    canvas.create_rectangle(101, 349 - x * 250/cap_x, 299, 349, fill="lightgreen")

    canvas.create_line(500, 100+250/cap_x, 500, 350, width=3)
    canvas.create_line(700, 100+250/cap_x, 700, 350, width=3,smooth=True)
    canvas.create_line(500, 350, 700, 350, width=3)
    canvas.create_rectangle(501, 349 - y * 250/cap_x, 699, 349, fill="slateblue")

    x_text = f"x: {x}"
    y_text = f"y: {y}"
    canvas.create_text(100, 380, text=x_text, font=("Helvetica", 16), fill="black", anchor="w")
    canvas.create_text(500, 380, text=y_text, font=("Helvetica", 16), fill="black", anchor="w")
    
    # Display applied rule
    canvas.create_text(400, 420, text=rule, font=("Helvetica", 18, "bold"), fill="blue")

def print_state(x, y, s):
    print(f"({x}, {y}), {s}")

def process_next_state(q, visited, cap_x, cap_y, target, canvas):
    if q:
        state = q.popleft()
        x, y = state[0]
        s = state[1]

        if x < 0 or x > cap_x or y < 0 or y > cap_y:
            process_next_state(q, visited, cap_x, cap_y, target, canvas)
            return

        if x == target:
            visited[x][y] = True
            create_jug(canvas, x, y, s)
            print("Solution found:")
            print_state(x, y, s)
            root.after(1000, process_next_state , q, visited, cap_x, cap_y, target, canvas)
            return

        visited[x][y] = True

        print_state(x, y, s)

        create_jug(canvas, x, y, s)

        if x < cap_x and not visited[cap_x][y]:
            q.append(((cap_x, y), "Rule 1"))
            visited[cap_x][y] = True

        if y < cap_y and not visited[x][cap_y]:
            q.append(((x, cap_y), "Rule 2"))
            visited[x][cap_y] = True

        d = cap_y - y
        if x > 0 and not visited[x - d][d]:
            q.append(((x - d, d), "Rule 3"))
            visited[x - d][d] = True

        c = cap_x - x
        if y > 0 and not visited[c][y - c]:
            q.append(((c, y - c), "Rule 4"))
            visited[c][y - c] = True

        if x > 0 and not visited[0][y]:
            q.append(((0, y), "Rule 5"))
            visited[0][y] = True

        if y > 0 and not visited[x][0]:
            q.append(((x, 0), "Rule 6"))
            visited[x][0] = True

        if ((x + y) > cap_x) and (y > 0) and not visited[cap_x][y - (cap_x - x)]:
            q.append(((cap_x, y - (cap_x - x)), "Rule 7"))
            visited[cap_x][y - (cap_x - x)] = True

        if ((x + y) > cap_y) and (x > 0) and not visited[x - (cap_y - y)][cap_y]:
            q.append(((x - (cap_y - y), cap_y), "Rule 8"))
            visited[x - (cap_y - y)][cap_y] = True

        if ((x + y) <= cap_x) and (y > 0) and not visited[x + y][0]:
            q.append(((x + y, 0), "Rule 9"))
            visited[x + y][0] = True

        if ((x + y) <= cap_y) and (x > 0) and not visited[0][x + y]:
            q.append(((0, x + y), "Rule 10"))
            visited[0][x + y] = True

        root.after(1000, process_next_state , q, visited, cap_x, cap_y, target, canvas)

def solve(cap_x, cap_y, target, canvas):
    q = deque()
    visited = [[False for _ in range(cap_x + 1)] for _ in range(cap_x + 1)]

    q.append(((0, 0), "initial"))

    process_next_state(q, visited, cap_x, cap_y, target, canvas)


def update_values():
    global cap_x, cap_y, target
    cap_x = int(jug_x_entry.get())
    cap_y = int(jug_y_entry.get())
    target = int(target_entry.get())
    canvas.delete("all")
    solve(cap_x, cap_y, target, canvas)

if __name__ == "__main__":
    

    canvas_frame = Frame(root)
canvas_frame.pack(side=LEFT)
canvas = Canvas(canvas_frame, width=800, height=500)
canvas.pack()


# Create and pack a frame for the input fields and buttons
input_frame = Frame(root)
input_frame.pack(side=LEFT,padx=10,pady=10)
# Label and Entry for Jug X Capacity
jug_x_label = Label(input_frame, text="Jug X Capacity:")
jug_x_label.pack()
jug_x_entry = Entry(input_frame)
jug_x_entry.pack()

# Label and Entry for Jug Y Capacity
jug_y_label = Label(input_frame, text="Jug Y Capacity:")
jug_y_label.pack()
jug_x_entry.config(fg="blue")
jug_y_entry = Entry(input_frame)
jug_y_entry.config(fg="blue")
jug_y_entry.pack()

# Label and Entry for Target Quantity
target_label = Label(input_frame, text="Target Quantity:",)
target_label.pack()
target_entry = Entry(input_frame)
target_entry.config(fg="blue")
target_entry.pack()

# Button to Solve
update_button = Button(input_frame, text="Solve", command=update_values,pady=10,padx=10)
update_button.pack()

# root.configure(bg="#FF69B4")  # Set a light background color for the window
mylabel.config( fg="blue")  # Adjust label colors




root.mainloop()
