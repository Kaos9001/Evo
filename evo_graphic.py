import pygame as pg
import sys

class Renderer:
	def __init__(self,size):
		self.screen = pg.display.set_mode(size)
		self.size = size
	def draw_dot(self,position,radius,color):
		pg.draw.circle(self.screen,color,position,radius,0)
	def start(self):
		pg.init()
	def update(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit(); sys.exit();
		pg.display.update()
		self.screen.fill((255,255,255))