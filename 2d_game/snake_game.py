import pyglet
from pyglet import shapes
from DIPPID import SensorUDP
import random


WIDTH = 800
HEIGHT = 600
win = pyglet.window.Window(WIDTH, HEIGHT)

batch = pyglet.graphics.Batch()

sensor = SensorUDP(5700)


BLOCK = 20

snake = [(400, 300)]
direction = (BLOCK, 0)

food = (random.randrange(0, WIDTH, BLOCK),
        random.randrange(0, HEIGHT, BLOCK))

score = 0


def update(dt):
    global snake, direction, food, score

    acc = sensor.get_value("accelerometer")

    # Direction logic based on accelerometer
    if acc:
        x = acc["x"]
        y = acc["y"]

        if x > 0.5:
            direction = (BLOCK, 0)
        elif x < -0.5:
            direction = (-BLOCK, 0)
        elif y > 0.5:
            direction = (0, BLOCK)
        elif y < -0.5:
            direction = (0, -BLOCK)

    # move snake
    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])

    snake.insert(0, new_head)

    # food collision
    if new_head == food:
        score += 1
        food = (random.randrange(0, WIDTH, BLOCK),
                random.randrange(0, HEIGHT, BLOCK))
    else:
        snake.pop()

    # wall collision
    if (new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT):
        reset()

    # self collision
    if new_head in snake[1:]:
        reset()


def reset():
    global snake, score, direction
    snake = [(400, 300)]
    direction = (BLOCK, 0)
    score = 0


@win.event
def on_draw():
    win.clear()

    # snake
    for segment in snake:
        shapes.Rectangle(segment[0], segment[1],
                         BLOCK, BLOCK,
                         color=(0, 255, 0),
                         batch=batch).draw()

    # food
    shapes.Rectangle(food[0], food[1],
                     BLOCK, BLOCK,
                     color=(255, 0, 0),
                     batch=batch).draw()

    # score
    label = pyglet.text.Label(
        f"Score: {score}",
        x=10, y=HEIGHT - 30
    )
    label.draw()



pyglet.clock.schedule_interval(update, 0.1)
pyglet.app.run()