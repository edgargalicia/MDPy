
from Tkinter import *
root = Tk()
w = Canvas(root, width=400, height=400, bg='#aaaaaa')

w.create_line(0,300,300,300,300,0,fill='yellow')
w.pack()

p=[]

class M:
    def __init__(self, rx, ry, vx=0, vy=0, fx=0, fy=0, links=()):
        self.rx, self.ry = rx,ry
        self.vx, self.vy = vx,vy
        self.fx, self.fy = fx,fy
        self.links = [ (link, w.create_line(0,0,0,0,fill='red')) for link in links if link != False ]
        self.p = w.create_oval(self.rx, self.ry, self.rx+1, self.ry+1, fill='black')
    def show_up(self):
        w.coords(self.p, self.rx, self.ry, self.rx+5, self.ry+5)
        for link in self.links:
            w.coords(link[1], p[link[0]].rx+2, p[link[0]].ry+2, self.rx, self.ry)
    def clear(self):
        w.delete(self.p)
        for link in self.links:
            w.delete(link[1])
        self.links=[]
    def __str__(self): return 'r(%s,%s); v(%s,%s); f(%s,%s)'%(self.rx, self.ry, self.vx, self.vy, self.fx, self.fy)

#build gum net
side = 4
b1 = lambda x,y: x<side-1 and x+1+y*side
b2 = lambda x,y: y<side-1 and x+(y+1)*side
b3 = lambda x,y: x<side-1 and y<side-1 and x+1+(y+1)*side
net = lambda m,n: [ M(x*13+m, y*13+n, 0, 0, 0, 0, (b1(x,y), b2(x,y), b3(x,y)))
                   for y in xrange(side)
                   for x in xrange(side) ]

def compute_force(m):
    for n in m.links:
        len = ((m.rx - p[n[0]].rx)**2 + (m.ry - p[n[0]].ry)**2)**0.5
        f = ((len - 20)*4)**3
        m.fx += -(f/len) * (m.rx - p[n[0]].rx)
        m.fy += -(f/len) * (m.ry - p[n[0]].ry)
        p[n[0]].fx += (f/len) * (m.rx - p[n[0]].rx)
        p[n[0]].fy += (f/len) * (m.ry - p[n[0]].ry)

def clear_force(m):
    m.fx = 0
    m.fy = 0

def compute_speed(m):
    m.vx += 0.03*m.fx
    m.vy += 0.03*m.fy
    if m.rx>300 or m.rx<0: m.vx=0
    if m.ry>300 or m.ry<0: m.vy=0

def compute_position(m):
    m.rx += 0.001*m.vx
    m.ry += 0.001*m.vy

def compute_attenuation(m):
    m.vx *= 0.99
    m.vy *= 0.99

def compute_gravity(m):
    m.fx += 0
    m.fy += 100

def frame():
    print '------<next frame>------'
    map(clear_force, p)
    map(compute_force, p)
    map(compute_gravity, p)
    map(compute_speed, p)
    map(compute_attenuation, p)
    map(compute_position, p)
    for o in p: o.show_up()
    root.after(10, frame)
frame()

def klik(event):
    print 'create new gum net'
    r = net(event.x, event.y)
    for n in p: n.clear()
    while p: p.pop()
    for n in r: p.append(n)
    for n in r: print n; n.show_up()
root.bind("<Button-1>", klik)

root.mainloop()
