from cocos.tiles import RectMapLayer, RectCell, TileSet

class Dungeon(RectMapLayer):
	def __init__(self, width, height, th=16, tw=16):
		self.tile_set = TileSet.from_atlas("ground", 0, "img/tileset_min_cave.png", tw, th)

		# make every cell collidable
		properties = {'top': True, 'bottom': True, 'right': True, 'left': True}

		cells = []
		for i in range(width):
			c = []
			for j in range(height):
				tile = self.tile_set[3]
				cell = RectCell(i, j, tw, th, properties, tile)
				c.append(cell)
			cells.append(c)

		super(Dungeon, self).__init__('cave', tw, th, cells)


	def make_walkable(self, walkable):
		for tile in walkable:
			cell = self.get_cell(*tile)
			if cell is not None:
				# walkable area should not be collidable
				cell['top'] = cell['bottom'] = cell['right'] = cell['left'] = False
				cell.tile = self.tile_set[0]
