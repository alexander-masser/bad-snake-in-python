from tkinter import *
from time import sleep
from random import randint
from PIL import Image, ImageTk

height = 500
width = 500
grid_length = 23
direction = (1, 0)
number_bodies = 10
bodies = []

number_board_fields = 20
x_left = 20
y_up = 20
x_right = x_left + number_board_fields * grid_length
y_down = y_up + number_board_fields * grid_length

start_position = [x_left + grid_length * 0.5 + number_board_fields //2*grid_length,
                 y_up + grid_length * 0.5 + number_board_fields//2*grid_length]

head_position = start_position

window = Tk()
window.title("Snake")
canvas = Canvas(window, width=width, height=height)
canvas.pack()

body_image = Image.open("images/body.jpg")
body_image = body_image.resize((grid_length, grid_length), Image.Resampling.LANCZOS)
body_image = ImageTk.PhotoImage(body_image)

canvas.create_line(x_left, y_up, x_left, y_down, width=5)
canvas.create_line(x_right, y_up, x_right, y_down, width=5)
canvas.create_line(x_left, y_up, x_right, y_up, width=5)
canvas.create_line(x_left, y_down, x_right, y_down, width=5)


def move_head():
    head_position[0] += direction[0] * grid_length
    head_position[1] += direction[1] * grid_length


def new_body():
    bodies.append(
        canvas.create_image(head_position[0], head_position[1], image=body_image)
    )


def delete_old_body():
    if len(bodies) > number_bodies:
        canvas.delete(bodies.pop(0))


def change_direction(event):
    global direction
    if event.keysym == "w":
        if direction != (0, 1):
            direction = (0, -1)
    if event.keysym == "s":
        if direction != (0, -1):
            direction = (0, 1)
    if event.keysym == "a":
        if direction != (1, 0):
            direction = (-1, 0)
    if event.keysym == "d":
        if direction != (-1, 0):
            direction = (1, 0)


canvas.bind_all("<Key>", change_direction)


def is_outside_board():
    return (head_position[0] < x_left or head_position[0] > x_right or
    head_position[1] < y_up or head_position[1] > y_down)


def does_head_bite_body():
    for body in bodies:
        x, y = canvas.coords(body)
        if head_position[0] == x and head_position[1] == y:
            return True
    return False


lunch_img = Image.open("images/mouse.jpg")
lunch_img = lunch_img.resize((grid_length, grid_length), Image.Resampling.LANCZOS)
lunch_img = ImageTk.PhotoImage(lunch_img)


lunch_position = [50, 60]


def generate_lunch_position():
    while True:
        candidate = [x_left + grid_length*0.5 + randint(0, number_board_fields-1)*grid_length,
                     y_up + grid_length*0.5 + randint(0, number_board_fields-1)*grid_length]
        candidate_valid = True
        for body in bodies:
            x, y = canvas.coords(body)
            if x == candidate[0] and y == candidate[1]:
                candidate_valid = False

        if candidate_valid:
            return candidate


lunch = None


def draw_lunch():
    global lunch
    if lunch is not None:
        canvas.delete(lunch)
    lunch = canvas.create_image(lunch_position[0], lunch_position[1], image=lunch_img)


def head_eats_lunch():
    return head_position[0] == lunch_position[0] and head_position[1] == lunch_position[1]



sleep_time = 0.1
while True:
    lunch_position = generate_lunch_position()

    draw_lunch()
    direction = (1, 0)
    head_position = list(start_position)
    for body in bodies:
        canvas.delete(body)

    bodies=[]
    number_bodies = 10

    while True:
        move_head()

        if does_head_bite_body():
            break

        new_body()
        delete_old_body()

        if head_eats_lunch():
            lunch_position = generate_lunch_position()
            draw_lunch()
            number_bodies += 1

        if is_outside_board():
            break

        window.update()
        sleep(sleep_time)