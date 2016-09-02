import pygame as pg
import sys

class Renderer:
	def __init__(self,size):
		self.screen = pg.display.set_mode(size)
	def draw_dot(self,position,radius,color):
		pg.draw.circle(self.screen,color,position,radius,0)
	def start_loop(self):
		pg.init()
		while True:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					pg.quit(); sys.exit();
			self.screen.fill((255,255,255))
			pg.display.update()