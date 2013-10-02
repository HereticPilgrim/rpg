from pyglet.window import key

import cocos
from cocos.scene import Scene
from cocos.tiles import ScrollingManager

class GameScene(Scene):

	def __init__(self):
		super(GameScene, self).__init__()

		self.scroller = ScrollingManager()
		self.add(self.scroller)

		self.load('test_map.tmx')

		collision_layer = self.map.get_resource('collision')

		# initialise player layer
		self.player_layer = PlayerLayer(self.scroller, collision_layer)
		self.scroller.add(self.player_layer, z=50)

		self.schedule(self.update)

	def update(self, dt):
		"""Updates the game every frame, approx. 1/60 secs."""
		self.player_layer.update(dt)


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

	def __init__(self, scroller, collision_map):
		super(PlayerLayer, self).__init__()
		self.scroller = scroller

		player = cocos.sprite.Sprite('img/octocat.png')
		self.add(player, name='player')
		# player.do(PlayerController(self.keys_pressed, collision_map, scroller))


	def on_key_press(self, k, mod):
		self.keys_pressed.add(k)


	def on_key_release(self, k, mod):
		self.keys_pressed.remove(k)


	def draw(self):
		# need to call parent draw() first, otherwise cocos is confused.
		super(PlayerLayer, self).draw()


	def update(self, dt):
		# key_names = [key.symbol_string (k) for k in self.keys_pressed]


		pass



# class PlayerController(cocos.actions.Action, cocos.tiles.RectMapCollider):
# 
# 	def __init__(self, keys_pressed, collision_map, scroller):
# 		self.keys_pressed = keys_pressed
# 		self.collision_map = collision_map
# 		self.scroller = scroller

# 	def step(self, dt):
# 		print self.keys_pressed
# 		# dx, dy = self.target.velocity

# 		# # using the player controls, gravity and other acceleration influences
# 		# # update the velocity
# 		# dx = (keyboard[key.RIGHT] - keyboard[key.LEFT]) * self.MOVE_SPEED *dt
# 		# dy = dy + self.GRAVITY * dt
# 		# if self.on_ground and keyboard[key.SPACE]:
# 		# 	dy = self.JUMP_SPEED

# 		# # get the player's current bounding rectangle
# 		# last = self.target.get_rect()
# 		# new = last.copy()
# 		# new.x += dx
# 		# new.y += dy * dt

# 		# # run the collider
# 		# dx, dy = self.target.velocity = self.collide_map(tilemap, last, new, dy, dx)
# 		# self.on_ground = bool(new.y == last.y)

# 		# # player position is anchored in the center of the image rect
# 		# self.target.position = new.center

# 		# # move the scrolling view to center on the player
# 		# scroller.set_focus(*new.center)



cocos.director.director.init(width=800, height=600, caption='Testing', do_not_scale=True)

main_scene = GameScene()

cocos.director.director.run(main_scene)