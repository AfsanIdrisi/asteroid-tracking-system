import tkinter as tk
from utility import (
    load_assets, animate_earth, rotate_radar,
    spawn_asteroid, updateAsteroids, update_status
)

S_WIDTH = 1000
S_HEIGHT = 500

root = tk.Tk()
root.geometry(f"{S_WIDTH}x{S_HEIGHT}")
root.title("Asteroid Radar System")

canvas = tk.Canvas(root, width=S_WIDTH, height=S_HEIGHT)
canvas.pack()

assets = load_assets(canvas, S_WIDTH, S_HEIGHT)

asteroids = []

animate_earth(canvas, S_WIDTH, S_HEIGHT, assets, root)
rotate_radar(canvas, S_WIDTH, S_HEIGHT, 0, assets, root)
spawn_asteroid(canvas, asteroids, assets, root)
updateAsteroids(canvas, asteroids, root)

root.mainloop()
