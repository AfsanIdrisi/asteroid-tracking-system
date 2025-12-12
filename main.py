import tkinter as tk
import math
from PIL import Image, ImageTk
from utility import rotate_radar,spawn_asteroid,updateAsteroids
root = tk.Tk()
root.title("Asteroid Radar Simulation")
asteroids = []

swidth = 1000
shight = 500

root.geometry(f"{swidth}x{shight}")

canvas = tk.Canvas(root,width=swidth,height=shight,bg="black")
canvas.pack()

radar_img = Image.open("./asset/radar.png").resize((250,250))

tk_radar = ImageTk.PhotoImage(radar_img)

angle =0

rotate_radar(canvas,swidth,shight,angle,tk_radar,radar_img,root)
spawn_asteroid(canvas,asteroids,root)
updateAsteroids(canvas,root,asteroids)
root.mainloop()