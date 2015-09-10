#---------------------------------------
# To Do:
# update the colors of edges based upon the colors of the vertices that are connected.
#---------------------------------------
# Every edge stores the indices of the vertices which made it.

import matplotlib as mpl
import numpy as np
import random
import networkx as nx
import sys
import math


mpl.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import Tkinter as Tk

mpl.rcParams['toolbar'] = 'None'

class GraphApp:
	def __init__(self, canvas, fig, ax1):	
		self.fig = fig
		self.ax = ax1
		self.vert_x = []
		self.vert_y = []
		self.canvas = canvas
		self.canvas.mpl_connect('button_press_event', self.onClick)
		self.canvas.show()
		self.r = []
		self.c = []
		self.edge_indices = [] # This stores tuples of the indices of vertices which are connected by an edge.
		self.edge_colors = []
		self.edge_X = []
		self.edge_Y = []
		self.temp_X = []
		self.temp_Y = []
		self.clicks = 0
		self.tol = 1e-1
		self.near = 0
		#self.G = nx.Graph()
		self.i = 0
		self.colors = {0:0, 1:50}

	def onClick(self, event):
		self.near, self.x_coord, self.y_coord = self.distance(event.xdata, event.ydata)
		if self.near == 0:
			self.clicks = 0
                        self.temp_X = []
			self.temp_Y = []
			self.vert_x.append(event.xdata)
			self.vert_y.append(event.ydata) # Dot ready for drawing.
			self.r.append(100)
			#self.G.add_node(self.i) # Add a node to the graph
			self.i += 1
                        self.c.append(0)
		else: # then the click is close
                        if self.clicks == 1 and self.temp_X != [] and self.temp_X[0] == self.x_coord and self.temp_Y[0] == self.y_coord:
                                self.clicks = 0
                                self.temp_X = []
				self.temp_Y = []
			elif self.clicks == 1: # Then we will draw a line
				self.clicks = 0
				self.temp_X.append(self.x_coord)
				self.temp_Y.append(self.y_coord)
				self.edge_X.append(self.temp_X)
				self.edge_Y.append(self.temp_Y)
				e = (self.vert_x.index(self.temp_X[0]), self.vert_x.index(self.temp_X[1]))
				edge_idx_tup = (self.vert_x.index(self.temp_X[1]), self.vert_x.index(self.temp_X[0]))
				self.edge_colors.append('0.75')
				#self.G.add_edge(*e)
				self.temp_X = []
				self.temp_Y = []
			else: # Just add a  dot to the list  
				self.clicks = 1
				self.temp_X.append(self.x_coord) # by value or by reference?
				self.temp_Y.append(self.y_coord)
		#A = nx.adjacency_matrix(self.G)
		for index in range(self.i):
                        #if self.G.degree(index) in self.colors:
                        #        self.c[index] = self.colors[self.G.degree(index)]
                        #else:
                        #        self.c[index] = 99
                #print self.c
			self.ax.scatter(self.vert_x,self.vert_y, s= self.r, c=self.c, cmap = mpl.cm.Blues)
		for j in range(len(self.edge_X)):
			self.ax.plot(self.edge_X[j], self.edge_Y[j], self.edge_colors[j])
		self.canvas.draw()
		
	def distance(self, x, y):
		"""Check all of the coordinates in the vert_x, vert_y lists. If there is a coordinate near to the input x, y 
		then return near = 1, and x, y equal the found coordinates."""
		for i, v in enumerate(self.vert_x):
			if math.sqrt((x - self.vert_x[i])**2+(y - self.vert_y[i])**2) < self.tol:
				return 1, self.vert_x[i], self.vert_y[i]
		return 0, x, y

	def clearPlot(self):
		self.fig.clear()
		self.vert_x = []
		self.vert_y = []
		self.edge_X = []
		self.edge_Y = []
		self.r = []
		self.c = []
		self.i = 0
		self.edge_colors = []
		self.edge_indices = []
		for index in range(self.i):
                        #if self.G.degree(index) in self.colors:
                        #        self.c[index] = self.colors[self.G.degree(index)]
                        #else:
                        #        self.c[index] = 99
                #print self.c
			self.ax.scatter(self.vert_x,self.vert_y, s= self.r, c=self.c, cmap = mpl.cm.Blues)
		for j in range(len(self.edge_X)):
			self.ax.plot(self.edge_X[j], self.edge_Y[j], self.edge_colors[j])
		self.canvas.draw()

if __name__ == '__main__':
	root = Tk.Tk()
	fig = Figure(facecolor = 'white')
	ax1 = fig.add_subplot('111')
	ax1.set_xlim(0,1)
	ax1.set_ylim(0,1)
	ax1.axis('off')
	canvas = FigureCanvasTkAgg(fig, master=root)
	cp = GraphApp(canvas, fig, ax1)
	canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
	
	def _quit():
		root.quit()     # stops mainloop
		root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate
	def _clear():
		cp.clearPlot()

	button = Tk.Button(master=root, text='Quit', command=_quit)
	button.pack(side=Tk.BOTTOM)
	button = Tk.Button(master=root, text='Clear', command=_clear)
	button.pack(side=Tk.BOTTOM)
	Tk.mainloop()