import matplotlib.pyplot as plt
import numpy as np
import random
import networkx as nx
import sys
import math

class GraphApp:
	def __init__(self, fig=None):	
		self.fig = plt.get_current_fig_manager().canvas.figure
		self.fig.canvas.mpl_connect('button_press_event', self.onClick)
		self.vert_x = []
		self.vert_y = []
		self.r = []
		self.c = []
		self.edge_X = []
		self.edge_Y = []
		self.temp_X = []
		self.temp_Y = []
		self.clicks = 0
		self.tol = 1e-1
		self.near = 0
		self.G = nx.Graph()
		self.i = 0

	def onClick(self, event):
		"""
		Check a click before anything else. A click is checked in the following way:
		If the click is close to a coordinate in the self.x and self.y lists, then either:
			The user has clicked another dot first OR
			The user has not.
			If a user has clicked another dot first then store the new coordinate in a list and draw a line between the two  dots.
			If a user has not, then simply store the new dot in a list.

		If a click is not close to another coordinate in self.x, self.y, then either:
			The user has clicked another dot previously OR
			The user has not.
			If the user has clicked another dot previously, then delete the coordinates from the list, and draw a new dot.
			Draw a new dot.
		"""
		self.near, self.x_coord, self.y_coord = self.distance(event.xdata, event.ydata)
		if self.near == 0:
			self.clicks = 0
			self.temp_X = []
			self.temp_Y = []
			self.vert_x.append(event.xdata)
			self.vert_y.append(event.ydata) # Dot ready for drawing.
			self.r.append(100)
			self.G.add_node(self.i) # Add a node to the graph
			self.i += 1
		else: # then the click is close
			if self.clicks == 1: # Then we will draw a line
				self.clicks = 0
				self.temp_X.append(self.x_coord)
				self.temp_Y.append(self.y_coord)
				self.edge_X.append(self.temp_X)
				self.edge_Y.append(self.temp_Y)
				e = (self.vert_x.index(self.temp_X[0]), self.vert_x.index(self.temp_X[1]))
				self.G.add_edge(*e)
				self.temp_X = []
				self.temp_Y = []
			else: # Just add a  dot to the list  
				self.clicks = 1
				self.temp_X.append(self.x_coord) # by value or by reference?
				self.temp_Y.append(self.y_coord)
		plt.scatter(self.vert_x,self.vert_y, s= self.r)#, c=self.c)
		for j in range(len(self.edge_X)):
			plt.plot(self.edge_X[j], self.edge_Y[j], 'b')
		self.fig.canvas.draw()
		A = nx.adjacency_matrix(self.G)
		print(A.todense())

	def distance(self, x, y):
		"""Check all of the coordinates in the vert_x, vert_y lists. If there is a coordinate near to the input x, y 
		then return near = 1, and x, y equal the found coordinates."""
		for i, v in enumerate(self.vert_x):
			if math.sqrt((x - self.vert_x[i])**2+(y - self.vert_y[i])**2) < self.tol:
				return 1, self.vert_x[i], self.vert_y[i]
		return 0, x, y

def showGraphApp(fig=None):
	cp = GraphApp(fig)
	plt.show()
	
if __name__ == '__main__':
	#plt.xkcd()
	fig = plt.figure(facecolor = 'white')
	ax1 = plt.subplot('111')
	ax1.set_xlim(0,1)
	ax1.set_ylim(0,1)
	plt.axis('off')
	cp = GraphApp(fig)
	plt.show()