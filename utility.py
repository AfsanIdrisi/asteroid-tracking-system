from PIL import Image, ImageTk
from Asteroid import Asteroid
import random
def draw_ship(canvas,swidth,shight):
    ship_w = 60
    ship_h = 30

    x1 = swidth//2 -ship_w//2
    y1 = shight//2 - ship_h//2
    x2 = x1+ship_w
    y2 = y1+ship_w
    canvas.create_rectangle(x1,y1,x2,y2,fill="white",outline="blue")

def rotate_radar(canvas,swidth,shight,angle,tk_radar,radar_img,root):

    angle = (angle+2) % 360
    rotated = radar_img.rotate(angle,resample=Image.BICUBIC,expand=True)

    tk_radar = ImageTk.PhotoImage(rotated)

    canvas.delete("radar")
    canvas.create_image(swidth//2,shight//2, image=tk_radar,anchor="center")
    draw_ship(canvas,swidth,shight)
    root.after(30,rotate_radar,canvas,swidth,shight,angle,tk_radar,radar_img,root)




def spawn_asteroid(canvas,asteroids,root):
    a =Asteroid(canvas,random.uniform(2,4), random.randint(6,12))
    asteroids.append(a)
    root.after(10000,spawn_asteroid,canvas,asteroids,root)



def updateAsteroids(canvas,root,asteroids):
    alive = []
    for a in asteroids:
        if(a.update()):
            alive.append(a)
    asteroids [:] = alive
    root.after(30, updateAsteroids,canvas,root,asteroids)