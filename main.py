from pyglet.window import key

import cocos
from cocos.scene import Scene
from cocos.tiles import ScrollingManager

from DungeonGenerator import *

class GameScene(Scene):

	def __init__(self):
		super(GameScene, self).__init__()

		self.scroller = ScrollingManager()
		self.add(self.scroller)

		w = h = 50

		self.dungeon_generator = DungeonGenerator()
		self.generate_dungeon(w,h)

		self.scroller.add(self.dungeon_map)

		self.schedule(self.update)


	def update(self, dt):
		"""Updates the game every frame, approx. 1/60 secs."""
		pass
	

	def generate_dungeon(self, width, height):
		self.dungeon_map = self.dungeon_generator.generate(width, height)




cocos.director.director.init(width=800, height=600, caption='Testing', do_not_scale=True)

main_scene = GameScene()

cocos.director.director.run(main_scene)