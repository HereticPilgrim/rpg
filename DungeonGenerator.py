from __future__ import division # needed because of stupid number/number=int legacy
from PerlinNoiseGenerator import PerlinNoiseGenerator

from cocos import tiles

from Dungeon import *


class DungeonGenerator:
	def __init__(self):
		self.heightmap = []


	def make_map(self, walkable):
		return walkable

	def generate(self, width, height):
		"""
			Generates the dungeon according to the following steps, similar to A* algorithm:
			* Determine entrance.
			* Determine exit.
			* Start at the entrance.
			* Calculate weighting function for every adjacent tile.
			* Make tile with lowest weighting value walkable.
			* Calculate weighting function for adjacent tiles of newly added tile.
			* Repeat last two steps until exit is reached.

			Returns Dungeon map
		"""
		self.width = width
		self.height = height

		self.start_x = width-5
		self.start_y = height-5

		self.exit_x = 5
		self.exit_y = 5

		# generate the heightmap and weights
		self.generate_heightmap()
		self.calculate_weights()

		# make tiles walkable where the player should be able to move
		walkable_area = self.generate_walkable()

		# create an empty dungeon map and pave walkable area
		dungeon_map = Dungeon(width, height, 16,16)
		dungeon_map.make_walkable(walkable_area)

		# return map
		return dungeon_map


	def calculate_weights(self):
		""" 
			Calculates the weights for each tile and stores it in self.weights for
			faster look-up.
		"""
		# clear weights
		self.weights = []
		# generate weighting values for every tile
		for x in range(self.width):
			row = []
			for y in range(self.height):
				w = self.weighting_function(x,y)
				row.append(w)
			self.weights.append(row)


	def weighting_function(self, x,y):
		""" Weighting function determines whether or not tile at (x,y) is turned into walkable floor
			or wall.
			Takes into account (descending order of importance):
			* How high the tile value is (heightmap). High = solid rock, low = normal earth.
			  Low values rather give a walkable tile than solid rock.
			* How far the tile is from the exit. Gives a slight trend towards the exit (negative weight!)
			# * How far the tile is from the map borders. The farther from the map border, the more likely
			  to be a walkable tile.
		"""
		w = self.heightmap[x][y] - ((x-self.exit_x)**2 + (y-self.exit_y)**2)/(self.width*self.height)
		return w



	def generate_heightmap(self):
		"""
			Generates the heightmap using Perlin noise.
		"""
		# clear heightmap
		self.heightmap = []

		# generate coarse new heightmap
		p = PerlinNoiseGenerator()
		p.generate_noise(self.width, self.height, 3, 3)

		# smooth heightmap
		for y in range(self.width):
			smoothed_row = []
			for x in range(self.height):
				smoothed_row.append(p.smooth_noise(x,y))
			self.heightmap.append(smoothed_row)


	def generate_walkable(self):
		"""
			Generates the walkable area according to the following steps, similar to A* algorithm:
			* Start at the entrance.
			* Calculate weighting function for every adjacent tile.
			* Make tile with lowest weighting value walkable.
			* Calculate weighting function for adjacent tiles of newly added tile.
			* Repeat last two steps until exit is reached.
		"""
		# tiles already considered in the dungeon generation (opened)
		opened = []
		opened.append( (self.start_x, self.start_y) )

		# tiles added to walkable area
		walkable = []
		walkable.append( (self.start_x, self.start_y) )

		exit_reached = False

		while not exit_reached:
			min_weight = float("Inf")
			min_weight_tile = None
			
			# find lowest weight
			for tile in opened:
				x, y = tile

				if self.weights[x][y] < min_weight:
					min_weight = self.weights[x][y]
					min_weight_tile = tile

			# print min_weight, min_weight_tile
			x,y = min_weight_tile

			# close min_weight tile and add to walkable
			opened.remove(min_weight_tile)
			walkable.append(min_weight_tile)

			# open adjacent unopened tiles
			if x+1 < self.width and x-1 > 0:
				if (x+1,y) not in opened and (x+1,y) not in walkable:
					opened.append((x+1,y))
				if (x-1,y) not in opened and (x-1,y) not in walkable:
					opened.append((x-1,y))
			if y+1 < self.height and y-1 > 0:
				if (x,y+1) not in opened and (x,y+1) not in walkable:
					opened.append((x,y+1))
				if (x,y-1) not in opened and (x,y-1) not in walkable:
					opened.append((x,y-1))

			# stop generation once exit is reached
			if x == self.exit_x and y == self.exit_y:
				exit_reached = True

		return walkable