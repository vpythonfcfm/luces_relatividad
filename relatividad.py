import numpy as np
from vpython import *

c = 10
v = 8
gamma = 1/np.sqrt(1-(v/c)**2)


color_off = color.white*0.5
color_on = color.yellow

def lorentz(luces): # aplica transf de lorentz a una lista de luces
	for luz in luces:
		dt = luz.dt
		luz.dt = (dt-luz.pos.x*v/c**2)*gamma
		luz.pos.x = (luz.pos.x-v*dt)*gamma
	return luces

class luz:
	#t0 = t cuando empieza a parpadear
	#dt = intervalo entre que se prende y apaga
	#pos = vector de posicion
	#lit = True si esta prendida False si apagada
	def __init__(self, pos, t0, dt):
		self.pos = pos
		self.dt = dt
		self.t0 = t0
		self.fig = sphere(pos=pos,radius=0.2, color=color_off)
		self.lit = False
	def prender(self):
		if not self.lit:
			self.fig.color = color_on
			self.lit=True
	def apagar(self):
		if self.lit:
			self.fig.color = color_off
			self.lit=False
	def bip(self):
		if self.lit: self.apagar()
		else: self.prender()

class tracker: 
	#almacena una lista de luces e itera en el tiempo, prendiendo y 
	# apagando las luces.
	def __init__(self,luces, dt):
		self.luces=luces
		self.luces_t = dict()
		for luz in self.luces: # luces_t asocia a cada luz, el tiempo
		# en el que se va a prender
			self.luces_t[luz] = luz.dt+luz.t0
		self.t = 0 #empieza con t = 0, dt es el paso de la iteracion
		self.dt = dt # no confundir con el dt de cada luz
		#print(self.luces_t)
	def step(self):
		self.t += self.dt
		for luz in self.luces:
			if (self.luces_t[luz] >= (self.t - self.dt/2) and 
				 self.luces_t[luz] < (self.t + self.dt/2)):
				luz.bip()
				self.luces_t[luz] = self.t+luz.dt

L1 = []
L2 = []
for i in range(1,5):
	L1.append(luz(vector(i,0,0), 0, 0.5))
	L2.append(luz(vector(-i,0,0), 0, 0.5))

T = tracker(lorentz(L1) + L2,0.01)
b = box(pos=vector(0,0,0), length=0.4, height=5, width=0.1)
t1 = text(text='v=0', align='center', color=color.white, pos=vector(-2.5,-2,0))
t2 = text(text='v=0.8c', align='center', color=color.white, pos=vector(2.5,-2,0))
while True:
	rate(60)
	T.step()
	
