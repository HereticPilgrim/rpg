import cocos
from cocos.scene import Scene
from cocos.tiles import ScrollingManager

class GameScene(Scene):

	def __init__(self):
		super(GameScene, self).__init__()

		self.scroller = ScrollingManager()
		self.add(self.scroller)

		self.load('test_map.tmx')

		self.schedule(self.update)


	def update(self, dt):
		"""Updates the game approx. every 1/60 secs."""
		pass


	def load(self, map_filename):
		"""Loads the specified map and makes the collision layer collidable."""
		# load the tiled map in TMX format (www.mapeditor.org)
		self.map = cocos.tiles.load_tmx(map_filename)

		# find collision layer
		collision_layer = self.map.get_resource('collision')
		# collision_layer['visible'] = False

		# make all cells in layer 'collision' collidable
		for row in collision_layer.cells:
			for cell in row:
				# set collision properties
				cell['top'] = cell['bottom'] = cell['right'] = cell['left'] = True

		for name, layer in self.map.findall(cocos.tiles.RectMapLayer):
			self.scroller.add(layer, name=name)




cocos.director.director.init(width=800, height=600, caption='Testing', do_not_scale=True)

main_scene = GameScene()

cocos.director.director.run(main_scene)