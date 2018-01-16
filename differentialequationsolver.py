
# let's solve and draw a pendulum's animation

from __future__ import division # this is the most important import
from __future__ import print_function
from matplotlib import pyplot as plot
from matplotlib import animation
import math
import pygame
import os
print("imports successful!")

def fuv(u,v):
	return -20*math.sin(u)-0.08*v

def fvu(v,u):
	return v

# for v
def u_update(h,t,y):
	k1 = h*fvu(t,y)
	k2 = h*fvu(t+h/2,y+k1/2)
	k3 = h*fvu(t+h/2,y+k2/2)
	k4 = h*fvu(t+h,y+k3)
	return (y+1/6*(k1+2*(k2+k3)+k4))

# for u
def v_update(h,t,y):
	k1 = h*fuv(t,y)
	k2 = h*fuv(t+h/2,y+k1/2)
	k3 = h*fuv(t+h/2,y+k2/2)
	k4 = h*fuv(t+h,y+k3)
	return (y+1/6*(k1+2*(k2+k3)+k4))


def draw(time, theta):
	plot.figure()
	plot.plot(time,theta, 'r')
	plot.xlabel("time")
	plot.ylabel("theta")
	plot.legend(loc='bottom right')
	plot.show()

width = 400
hieght = 400
fps = 60

class pivot(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((10,10))
		self.image.fill((0,0,255))
		self.rect = self.image.get_rect()
		self.rect.center = (width/2,hieght/2)

	def update(self):
		pass

class pendulum_bob(pygame.sprite.Sprite):
	def __init__(self,time,theta):
		self.time = time
		self.theta = theta
		pygame.sprite.Sprite.__init__(self)
		# these 2 are important and always needed
		# print the folder path containing this python file
		this_folder = os.path.dirname(__file__)
		print("log: We are working in {} folder".format(this_folder))
		#self.image = pygame.Surface((50,50))
		self.image = pygame.image.load(os.path.join(this_folder,'circle.png')).convert()
		self.image.set_colorkey((255,255,255))
		self.image = pygame.transform.scale(self.image, (20,20))
		#self.image.fill((0,255,0))
		self.rect = self.image.get_rect()
		self.rect.center = (width/2,hieght/2)
		self.speedx = 20
		self.speedy = 40
		self.dt = 0.1
	
	def other_update(self):
		self.rect.x += self.speedx*self.dt
		if self.rect.left > width:
			self.rect.right = 0
		if self.rect.right < 0:
			self.rect.left = width

		self.rect.y += self.speedy*self.dt
		if self.rect.bottom < 0:
			self.rect.top = hieght
		if self.rect.top > hieght:
			self.rect.bottom = 0


	def update(self):
		self.rect.x += self.speedx*self.dt
		self.rect.y += self.speedy*self.dt

		# collisions
		if self.rect.top < 0 or self.rect.bottom > hieght:
			self.speedy = -self.speedy
		if self.rect.left < 0 or self.rect.right > width:
			self.speedx = -self.speedx


# this function does the iterations
def main():
	"""
	# this is the equation that we are going to solve
	theta'' + (b/L)*theta' + (g/l)*math.sin(theta) = 0
	we shall convert this to a system of 2 differential equations of first order and then apply 
	rk-4 method to that system
	our system is now as following:
	v' = -a*math.sin(u)-b*v = f(u,v)
	u' = v = f(v,u)
	from this analogy that y' = f(t,y)
	"""
	
	# results lists
	theta = []
	thetaprime = []
	time = []
	starttime = 0
	h = 0.001 # this is the step size
	stoptime = 140
	# initial conditions:
	theta0 = 2*math.pi
	thetaprime0 = 0
	theta.append(theta0)
	thetaprime.append(thetaprime0)
	time.append(starttime)

	for i in range(0, 1000000):
		theta.append(u_update(h,thetaprime[i],theta[i]))
		thetaprime.append(v_update(h,theta[i],thetaprime[i]))
		time.append(starttime+i*h)
		if time[-1] >= stoptime:
			break	
	print('found {} values in theta vector'.format(len(theta)))
	# print theta

	# draw the function 
	draw(time=time, theta=theta)
	# animate here

	# pygame initiations begin here
	print('log: beginning pygame now!!!')
	pygame.init()
	screen = pygame.display.set_mode((width,hieght))
	pygame.display.set_caption('pendulum_man')
	clock = pygame.time.Clock()
	# create the group of sprites to draw on the screen
	sprites = pygame.sprite.Group()
	bob = pendulum_bob(time=time,theta=theta)
	sprites.add(bob)
	# let's make a simple pivot as well
	fulcrum = pivot()
	sprites.add(fulcrum)

	# game loop is here
	quit = False
	while not quit:
		clock.tick(fps)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit = True
		# update the sprites here
		sprites.update()
		# draw all sprites here
		screen.fill((0,0,0))
		sprites.draw(screen)
		# clean the screen
		pygame.display.flip()

	pygame.quit()

if __name__ == "__main__":
	main()




















