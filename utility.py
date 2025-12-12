from PIL import Image, ImageTk, ImageSequence
from Asteroid import Asteroid
import random
import math


DANGER_THRESHOLD = 75
UPDATE_MS = 30
ASTEROID_SPAWN_MS = 2000


def load_assets(canvas, swidth, shight):

    assets = {}

    bg_img = ImageTk.PhotoImage(Image.open("./asset/bg.jpg").resize((swidth, shight)))
    bg_id = canvas.create_image(0, 0, anchor="nw", image=bg_img)

    assets["bg_img"] = bg_img
    assets["bg_id"] = bg_id

    radar = Image.open("./asset/radar.png").convert("RGBA").resize((250, 250))
    assets["radar_img"] = radar
    assets["radar_tk"] = ImageTk.PhotoImage(radar)

    earth_frames = []
    gif = Image.open("./asset/earth.gif")
    for frame in ImageSequence.Iterator(gif):
        frame = frame.convert("RGBA").resize((70, 70))
        earth_frames.append(ImageTk.PhotoImage(frame))

    assets["earth_frames"] = earth_frames
    assets["earth_index"] = 0
    assets["earth_id"] = None

    ast = Image.open("./asset/asteroid.png").convert("RGBA").resize((40, 40))
    assets["asteroid_img"] = ImageTk.PhotoImage(ast)


    return assets

def animate_earth(canvas, swidth, shight, assets, root):
    frames = assets["earth_frames"]
    idx = assets["earth_index"]
    eid = assets["earth_id"]

    frame = frames[idx]

    if eid is None:
        eid = canvas.create_image(swidth//2, shight//2, image=frame, tags="earth")
    else:
        canvas.itemconfig(eid, image=frame)

    canvas.tag_raise("earth")
     

    assets["earth_index"] = (idx + 1) % len(frames)
    assets["earth_id"] = eid

    root.after(80, animate_earth, canvas, swidth, shight, assets, root)

def rotate_radar(canvas, swidth, shight, angle, assets, root):
    radar_img = assets["radar_img"]

    angle = (angle + 2) % 360
    rotated = radar_img.rotate(angle, resample=Image.BICUBIC, expand=True)
    radar_tk = ImageTk.PhotoImage(rotated)

    assets["radar_tk"] = radar_tk

    canvas.delete("radar")
    canvas.create_image(swidth//2, shight//2, image=radar_tk, tags="radar")

    canvas.tag_raise("earth")
     

    root.after(30, rotate_radar, canvas, swidth, shight, angle, assets, root)


def spawn_asteroid(canvas, asteroid_list, assets, root):
    img = assets["asteroid_img"]
    a = Asteroid(canvas, img, speed=random.uniform(2, 4), size=random.randint(24, 40))

    asteroid_list.append(a)

    canvas.tag_raise("asteroid")
    canvas.tag_raise("asteroid_text")
     

    root.after(ASTEROID_SPAWN_MS, spawn_asteroid, canvas, asteroid_list, assets, root)



def updateAsteroids(canvas, asteroid_list, root):
    alive = []
    for a in asteroid_list:
        if a.update():
            alive.append(a)
    asteroid_list[:] = alive

    root.after(UPDATE_MS, updateAsteroids, canvas, asteroid_list, root)

def update_status(canvas, asteroid_list, assets, root):
    status_id = assets["status_id"]

    danger = any(a.crash_probability() >= DANGER_THRESHOLD for a in asteroid_list)

    if danger:
        canvas.itemconfig(status_id, text="DANGER", fill="red")
    else:
        canvas.itemconfig(status_id, text="SAFE", fill="lime")

    canvas.tag_raise(status_id)

    root.after(100, update_status, canvas, asteroid_list, assets, root)
