import random,math
swidth = 800
shight = 500

class Asteroid:
    def __init__(self,canvas,speed=3,size=10):
        self.canvas = canvas
        self.size = size
        self.speed = speed
        self.spawn_side = random.choice(["top","right","left","bottom"])
        
        if self.spawn_side == "top":
            self.x = random.randint(0,swidth)
            self.y = -20
            self.dx = random.uniform(-1,1)
            self.dy = random.uniform(0.5,1)
        
        elif self.spawn_side == "bottom":
            self.x = random.randint(0,swidth)
            self.y = shight +20
            self.dx = random.uniform(-1,1)
            self.dy = random.uniform(-1,-0.5)


        elif self.spawn_side == "left" :
            self.x = -20;
            self.y = random.randint(0,shight)
            self.dx = random.uniform(-1,-0.5)
            self.dy = random.uniform(-1,1) 

        elif self.spawn_side == "right":
            self.x = swidth +20
            self.y = random.randint(0,shight)
            self.dx = random.uniform(-1,-0.5)
            self.dy  = random.uniform(-1,1)

        
        length = math.sqrt(self.dx**2+self.dy**2)
        self.dx /= length
        self.dy /= length

        self.id = canvas.create_oval(self.x - size, self.y - size,self.x + size,self.y +size,fill="white")
        print(self.id)
        self.text_id = canvas.create_text(self.x,self.y - size -10, fill="white",font=("Arial",12,"bold"))


    def crashProbability(self):
        ax, ay = self.dx, self.dy
        cx = (swidth//2) - self.x
        cy = (shight//2)-self.y

        c_len = math.sqrt(cx**2 + cy**2)
        cx /= c_len
        cy /= c_len

        dot = ax*cx + ay*cy
        angle = math.degrees(math.acos(max(min(dot,1),-1)))
        if(angle>90):
           return 0
        else:
            return int(((90-angle)/90)*100)
    
    def update(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        
        self.canvas.coords(
            self.id,
            self.x -self.size, self.y - self.size,
            self.x + self.size, self.y +self.size
        )

        prob = self.crashProbability()
        self.canvas.coords(self.text_id, self.x, self.y - self.size - 10)
        self.canvas.itemconfig(self.text_id, text=f"{prob}%")

        if(self.x < -50 or self.x > swidth + 50 or self.y < -50 or self.y > shight + 50):
            self.canvas.delete(self.text_id)
            return False
        return True
