import tkinter as tk
import math, random
from PIL import Image, ImageTk

# ===============================
#  ASTEROID CLASS
# ===============================
class Asteroid:
    def __init__(self, canvas, speed=3, size=10):
        self.canvas = canvas
        self.size = size
        self.speed = speed
        
        self.spawn_side = random.choice(["top", "bottom", "left", "right"])

        if self.spawn_side == "top":
            self.x = random.randint(0, swidth)
            self.y = -20
            self.dx = random.uniform(-1, 1)
            self.dy = random.uniform(0.5, 1)

        elif self.spawn_side == "bottom":
            self.x = random.randint(0, swidth)
            self.y = shight + 20
            self.dx = random.uniform(-1, 1)
            self.dy = random.uniform(-1, -0.5)

        elif self.spawn_side == "left":
            self.x = -20
            self.y = random.randint(0, shight)
            self.dx = random.uniform(0.5, 1)
            self.dy = random.uniform(-1, 1)

        elif self.spawn_side == "right":
            self.x = swidth + 20
            self.y = random.randint(0, shight)
            self.dx = random.uniform(-1, -0.5)
            self.dy = random.uniform(-1, 1)

        # normalize direction
        length = math.sqrt(self.dx**2 + self.dy**2)
        self.dx /= length
        self.dy /= length

        self.id = canvas.create_oval(
            self.x - size, self.y - size,
            self.x + size, self.y + size,
            fill="white", outline=""
        )

        # text label for crash probability
        self.text_id = canvas.create_text(
            self.x, self.y - size - 10,
            fill="red", font=("Arial", 12, "bold"),
            text="0%"
        )

    def crash_probability(self):
        # Direction asteroid is moving
        ax, ay = self.dx, self.dy

        # Direction toward ship (center)
        cx = (swidth//2) - self.x
        cy = (shight//2) - self.y

        c_len = math.sqrt(cx**2 + cy**2)
        cx /= c_len
        cy /= c_len

        # dot product → angle
        dot = ax*cx + ay*cy
        angle = math.degrees(math.acos(max(min(dot, 1), -1)))

        # convert angle → probability
        if angle > 90:
            return 0
        else:
            return int(((90 - angle) / 90) * 100)

    def update(self):
        # move asteroid
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

        self.canvas.coords(
            self.id,
            self.x - self.size, self.y - self.size,
            self.x + self.size, self.y + self.size
        )

        # update crash probability label
        prob = self.crash_probability()
        self.canvas.coords(self.text_id, self.x, self.y - self.size - 10)
        self.canvas.itemconfig(self.text_id, text=f"{prob}%")

        # remove asteroid if out of screen
        if (
            self.x < -50 or self.x > swidth + 50 or
            self.y < -50 or self.y > shight + 50
        ):
            self.canvas.delete(self.id)
            self.canvas.delete(self.text_id)
            return False

        return True

# ===============================
# RADAR ROTATION
# ===============================
def rotate_radar():
    global angle, tk_radar, radar_img

    angle = (angle + 2) % 360
    rotated = radar_img.rotate(angle, resample=Image.BICUBIC, expand=True)
    tk_radar = ImageTk.PhotoImage(rotated)

    canvas.delete("radar")
    canvas.create_image(swidth//2, shight//2, image=tk_radar,
                        anchor="center", tags="radar")
    draw_ship()

    root.after(30, rotate_radar)


# ===============================
# SHIP
# ===============================
def draw_ship():
    ship_w = 60
    ship_h = 30

    x1 = swidth//2 - ship_w//2
    y1 = shight//2 - ship_h//2
    x2 = x1 + ship_w
    y2 = y1 + ship_h

    canvas.create_rectangle(
        x1, y1, x2, y2,
        fill="red", outline="white", width=2,
        tags="ship"
    )


# ===============================
# ASTEROID SPAWNER
# ===============================
asteroids = []

def spawn_asteroid():
    a = Asteroid(canvas, speed=random.uniform(2, 4), size=random.randint(6, 12))
    asteroids.append(a)
    root.after(10000, spawn_asteroid)  # spawn every 10 seconds


def update_asteroids():
    alive = []
    for a in asteroids:
        if a.update():
            alive.append(a)

    asteroids[:] = alive
    root.after(30, update_asteroids)


# ===============================
# MAIN GUI
# ===============================
root = tk.Tk()
root.title("Asteroid Radar Simulator")

swidth = 800
shight = 500
root.geometry(f"{swidth}x{shight}")

canvas = tk.Canvas(root, width=swidth, height=shight, bg="black")
canvas.pack()

radar_img = Image.open("./asset/radar.png").resize((250, 250))
tk_radar = ImageTk.PhotoImage(radar_img)
angle = 0

# Start systems
rotate_radar()
draw_ship()
spawn_asteroid()
update_asteroids()

root.mainloop()
