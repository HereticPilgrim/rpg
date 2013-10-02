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

		# initialise player layer
		self.player_layer = PlayerLayer(self.scroller)
		self.scroller.add(self.player_layer, z=50)


	def update(self, dt):
		"""Updates the game approx. every 1/60 secs."""
		self.player_layer.update()


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


class PlayerLayer(cocos.layer.ScrollableLayer):

	# make the layer an event handler
	is_event_handler = True
	keys_pressed = set()

	def __init__(self, scroller):
		super(PlayerLayer, self).__init__()
		self.scroller = scroller


	def on_key_press(self, k, mod):
		self.keys_pressed.add(k)


	def on_key_release(self, k, mod):
		self.keys_pressed.remove(k)


	def draw(self):
		# need to call parent draw() first, otherwise cocos is confused.
		super(PlayerLayer, self).draw()


	def update(self, dt):
		pass


cocos.director.director.init(width=800, height=600, caption='Testing', do_not_scale=True)

main_scene = GameScene()

cocos.director.director.run(main_scene)