import math

S_WIDTH = 1000
S_HEIGHT = 500
SHIP_W = 70
SHIP_H = 70


class Asteroid:
    def __init__(self, canvas, img, speed=3, size=30):
        import random

        self.canvas = canvas
        self.img = img
        self.speed = speed
        self.size = size

        side = random.choice(["top", "bottom", "left", "right"])

        if side == "top":
            self.x = random.randint(0, S_WIDTH)
            self.y = -30
            self.dx = random.uniform(-1, 1)
            self.dy = random.uniform(0.5, 1)

        elif side == "bottom":
            self.x = random.randint(0, S_WIDTH)
            self.y = S_HEIGHT + 30
            self.dx = random.uniform(-1, 1)
            self.dy = random.uniform(-1, -0.5)

        elif side == "left":
            self.x = -30
            self.y = random.randint(0, S_HEIGHT)
            self.dx = random.uniform(0.5, 1)
            self.dy = random.uniform(-1, 1)

        else:
            self.x = S_WIDTH + 30
            self.y = random.randint(0, S_HEIGHT)
            self.dx = random.uniform(-1, -0.5)
            self.dy = random.uniform(-1, 1)

        length = math.sqrt(self.dx**2 + self.dy**2) or 1
        self.dx /= length
        self.dy /= length

        self.id = canvas.create_image(self.x, self.y, image=self.img)
        self.text_id = canvas.create_text(self.x, self.y - size, text="0%", fill="white")

    def crash_probability(self):
        sx = S_WIDTH // 2
        sy = S_HEIGHT // 2

        if abs(self.x - sx) < SHIP_W//2 and abs(self.y - sy) < SHIP_H//2:
            return 100

        ax, ay = self.dx, self.dy

        cx = sx - self.x
        cy = sy - self.y

        dist = math.sqrt(cx*cx + cy*cy)
        if dist == 0:
            return 100

        cx /= dist
        cy /= dist

        dot = max(min(ax*cx + ay*cy, 1), -1)

        angle = math.degrees(math.acos(dot))

        if angle > 90:
            return 0

        return int(((90 - angle) / 90) * 100)

    def update(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

        self.canvas.coords(self.id, self.x, self.y)
        prob = self.crash_probability()

        self.canvas.coords(self.text_id, self.x, self.y - self.size)
        stmt=""
        color=""
        if(prob>=75):
            stmt="Danger"
            color="red"
        else :
            stmt="Safe"
            color="lime"

        self.canvas.itemconfig(self.text_id, text=f"{prob}% {stmt}",fill=color,font=("Arial",14,"bold"))

        if self.x < -80 or self.x > S_WIDTH + 80 or self.y < -80 or self.y > S_HEIGHT + 80:
            self.canvas.delete(self.id)
            self.canvas.delete(self.text_id)
            return False

        return True
