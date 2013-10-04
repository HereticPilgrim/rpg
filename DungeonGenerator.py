from __future__ import division # needed because of stupid number/number=int legacy
from PerlinNoiseGenerator import PerlinNoiseGenerator

class DungeonGenerator:
	def __init__(self):
		self.heightmap = []


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
		w = self.heightmap[x][y] + ((x-self.exit_x)**2 + (y-self.exit_y)**2)/(self.width*self.height)
		return w


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
		"""
		self.width = width
		self.height = height

		# self.start_x = width-5
		# self.start_y = height-5
		self.start_x = 7
		self.start_y = 7

		self.exit_x = 5
		self.exit_y = 5

		# create an empty map with only unwalkable tiles
		##

		# generate the heightmap and weights
		self.generate_heightmap()
		self.calculate_weights()

		# make tiles where the player should be able to move walkable
		walkable = self.generate_walkable()
		for tile in walkable:
			pass


	def calculate_weights(self):
		# clear weights
		self.weights = []
		# generate weighting values for every tile
		for x in range(self.width):
			row = []
			for y in range(self.height):
				w = self.weighting_function(x,y)
				row.append(w)
			self.weights.append(row)


	def generate_heightmap(self):
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

			print min_weight, min_weight_tile
			x,y = min_weight_tile

			# close min_weight tile and add to walkable
			opened.remove(min_weight_tile)
			walkable.append(min_weight_tile)

			# open adjacent unopened tiles
			if (x+1,y) not in opened:
				opened.append((x+1,y))
			if (x-1,y) not in opened:
				opened.append((x-1,y))
			if (x,y+1) not in opened:
				opened.append((x,y+1))
			if (x,y-1) not in opened:
				opened.append((x,y-1))

			print opened

			# if x == self.exit_x and y == self.exit_y:
			if len(walkable) > 5:
				exit_reached = True

		return walkable