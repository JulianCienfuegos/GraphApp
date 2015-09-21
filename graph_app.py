#-------------------------------------
# To Do:
# update the colors of edges based upon the colors of the vertices that are connected.
#---------------------------------------
# Every edge stores the indices of the vertices which made it.
# Then we can go through all of the vertices and update the colors.

import matplotlib as mpl
import numpy as np
import numpy.linalg as la
import networkx as nx
import random
import sys
import math
import time
from params import *

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
		self.canvas = canvas
		self.canvas.mpl_connect('button_press_event', self.onClick)
		self.set_empty_arrays()
		self.clicks = 0
		self.tol = 1e-1
		self.near = 0
		self.num_verts = 0
		self.G = nx.Graph()
	
	@property
	def adj_mat(self):
		self.A = nx.to_numpy_matrix(self.G)
		self.A = np.asarray(self.A)
		for r in self.A:
			r /= la.norm(r, 1)
		return self.A

	def onClick(self, event):
		self.near, self.x_coord, self.y_coord = self.distance(event.xdata, event.ydata)
		if self.near == 0:
			self.clicks = 0
			self.temp_X = []
			self.temp_Y = []
			self.vert_x.append(event.xdata)
			self.vert_y.append(event.ydata) # Dot ready for drawing.
			self.r.append(200)
			color = random.randint(1,8)
			self.c.append(reverse_map[color])
			self.G.add_node(self.num_verts)
			e = (self.num_verts, self.num_verts)
			self.G.add_edge(*e)
			self.num_verts += 1
			# DRAW A VERTEX
			self.draw_vert(event.xdata, event.ydata, color)
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
				edge_idx_tup = (e)
				self.G.add_edge(*e)
				# DRAW AN EDGE
				self.draw_edge(self.temp_X, self.temp_Y)
				self.temp_X = []
				self.temp_Y = []
			else: # Just add a  dot to the list  
				self.clicks = 1
				self.temp_X.append(self.x_coord) 
				self.temp_Y.append(self.y_coord)
		#self.draw_plot()
		
	def distance(self, x, y):
		'''Check all of the coordinates in the vert_x, vert_y lists. If there is a coordinate near to the input x, y 
		then return near = 1, and x, y equal the found coordinates.'''
		for i, v in enumerate(self.vert_x):
			if math.sqrt((x - self.vert_x[i])**2+(y - self.vert_y[i])**2) < self.tol:
				return 1, self.vert_x[i], self.vert_y[i]
		return 0, x, y

	def clear_plot(self):
		self.ax.clear()
		self.ax.set_xlim(0,1)
		self.ax.set_ylim(0,1)
		self.ax.axis('off')
		self.set_empty_arrays()
		self.num_verts = 0
		self.edge_colors = []
		self.edge_indices = []
		self.draw_plot()
		self.G.clear()

	def set_empty_arrays(self):
		self.vert_x = []
		self.vert_y = []
		self.r = []
		self.c = []
		self.edge_indices = [] 
		self.edge_colors = []
		self.edge_X = []
		self.edge_Y = []
		self.temp_X = []
		self.temp_Y = []

	def color_iteration(self):
		''' This function updates the colors of the vertices using  a simple rule.'''
		c_nums = [color_map[c] for c in self.c]
		c_vec = np.dot(self.adj_mat, c_nums)
		self.c = [reverse_map[math.floor(i)] for i in c_vec]
		self.draw_plot()

	def draw_plot(self):
		''' This should be sped up because it takes a very long time when there are ten or so vertices.'''
		for index in range(self.num_verts):
			self.ax.scatter(self.vert_x,self.vert_y, s= self.r, c=self.c)
		for j in range(len(self.edge_X)):
			self.ax.plot(self.edge_X[j], self.edge_Y[j], c = edge_color)
		self.canvas.draw()

	def draw_edge(self, e_x, e_y):
		self.ax.plot(e_x, e_y, c = edge_color)
		self.canvas.draw()

	def draw_vert(self, v_x, v_y, v_color):
		self.ax.scatter(v_x, v_y, s = self.r, c = reverse_map[v_color])
		self.canvas.draw()
	# We need to define a little arithmetic for working with color names, because the color numbers aren't working correctly.

if __name__ == '__main__':
	root = Tk.Tk()
	fig = Figure(facecolor = 'white')
	ax1 = fig.add_subplot('111')
	ax1.set_xlim(0,1)
	ax1.set_ylim(0,1)
	ax1.axis('off')
	canvas = FigureCanvasTkAgg(fig, master=root)
	canvas.show()					
	cp = GraphApp(canvas, fig, ax1)
	canvas.get_tk_widget().pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)

	def _update_colors():
		num_iters = int(entry.get())
		for i in range(num_iters):
			cp.color_iteration()
			time.sleep(0.25)

	def _quit():
		root.quit()     
		root.destroy()  
                    
	def _clear():
		cp.clear_plot()

	def _view_adj():
		print(cp.adj_mat)

	label = Tk.Label(text='Num Iters')
	label.pack(side=Tk.TOP)
	entry = Tk.Entry(root, width=10)
	entry.pack(side=Tk.TOP)
	button = Tk.Button(master=root, text='Run', command=_update_colors, height = 2, width = 10)
	button.pack(side=Tk.TOP)
	button = Tk.Button(master=root, text='Adjacency', command=_view_adj, height = 2, width = 10)
	button.pack(side=Tk.TOP)
	button = Tk.Button(master=root, text='Clear', command=_clear, height = 2, width = 10)
	button.pack(side=Tk.TOP)
	button = Tk.Button(master=root, text='Quit', command=_quit, height = 2, width = 10)
	button.pack(side=Tk.TOP)
	Tk.mainloop()
