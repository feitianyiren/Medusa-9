"""
Level 1:
1 Snake
Green key
Grassy
Is essentially a tutorial

Level 2:
5 Snakes
Orange key
Dirty

Level 3:
10 Snakes
Yellow key
Sandy

Level 4:
20 Snakes
Blue key
Snowy

Level 5:
Medusa
Stony

TODO general: Make the levels, make the character, make the enemies, give each health, implement keys.
TODO after: Add stage progression and menus
Level 1: Completed
Level 2: Not started
Level 3: Not started
Level 4: Not started
Level 5: Not started


TODO ASAP:
Made movement smoother
Make ramps
"""

# Platformer

# Import the arcade library
import arcade

# Constants

# Screen sizing assigned here as constants. Measured in pixels.
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

# Scaling
# This is the scaling for the player sprite
SPRITE_SCALING_PLAYER = 0.91
SPRITE_SCALING_WALL = 0.92

# Viewport
# How many pixels to leave between player and the edge of the screen
VIEWPORT_MARGIN = 40
RIGHT_MARGIN = 150

# Physics
# Sets the movement speed
MOVEMENT_SPEED = 5
JUMP_SPEED = 14
GRAVITY = 0.7


def get_map(filename):
	# Loads an array based on a a .CSV file which is then turned into a map

	# Opens the file
	map_file = open(filename)

	# Creates an empty list that will hold the map
	map_array = []

	# Reads a line from the file
	for line in map_file:
		# Takes away the whitespace and the new lines
		line = line.strip()

		# Creates a list that splits whenever there's a comma (should be after each number)
		map_row = line.split(",")

		# The list is currently all in string format but we want it in integers. ie it is currently "1" and we want it as 1
		# This loop fixes that
		for index, item in enumerate(map_row):
			map_row[index] = int(item)

		# Adds the formatted row into the array
		map_array.append(map_row)

	return map_array


class Game(arcade.Window):
	# This class is the main window of the game

	# Initialiser
	def __init__(self):
		# Calls upon the parent class's initialiser
		super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Medusa")
		# Initialising the current_stage variable
		self.current_stage = 0

		# Lists for the player, walls, enemies and keys
		self.player_list = None
		self.wall_list = None
		self.snake_list = None
		self.key_list = None

		self.all_sprites_list = None

		self.player_sprite = None

		self.physics_engine = None

		# Used to view port
		self.view_left = 0
		self.view_bottom = 0

	# Custom method called setup which sets everything up so that the user can play
	def setup(self):
		# Set the background colour as "AMAZON"
		arcade.set_background_color(arcade.color.AMAZON)

		# Makes the lists into arcade sprite lists which allow us to manipulate them much more easily
		self.player_list = arcade.SpriteList()
		self.wall_list = arcade.SpriteList()
		self.snake_list = arcade.SpriteList()
		self.key_list = arcade.SpriteList()
		self.all_sprites_list = arcade.SpriteList()

		# Sets the current_stage variable as 0 each setup
		self.current_stage = 0

		# Sets up the player
		self.player_sprite = arcade.Sprite("character.png", SPRITE_SCALING_PLAYER)
		# Starting positions
		self.player_sprite.center_x = 100
		self.player_sprite.center_y = 270
		self.player_list.append(self.player_sprite)
		self.all_sprites_list.append(self.player_sprite)

		map_array = get_map("level_1_map.csv")

		# Loops through array and makes sprites
		for row_index, row in enumerate(map_array):
			for column_index, item in enumerate(row):
				"""
				For this map the numbers represent:
				-1 = empty
				0 = left grass
				1 = middle grass
				2 = right grass
				3 = dirt
				4 = left ramp
				5 = left ramp support
				6 = green lock
				"""
				if item == -1:
					continue
				elif item == 0:
					wall = arcade.Sprite("grassLeft.png", SPRITE_SCALING_WALL)
				elif item == 1:
					wall = arcade.Sprite("grassMid.png", SPRITE_SCALING_WALL)
				elif item == 2:
					wall = arcade.Sprite("grassRight.png", SPRITE_SCALING_WALL)
				elif item == 3:
					wall = arcade.Sprite("grassCenter.png", SPRITE_SCALING_WALL)
				elif item == 4:
					wall = arcade.Sprite("grassHillLeft.png", SPRITE_SCALING_WALL)
				elif item == 5:
					wall = arcade.Sprite("grassHillLeft2.png", SPRITE_SCALING_WALL)
				elif item == 6:
					wall = arcade.Sprite("lock_green.png", SPRITE_SCALING_WALL)

				# Calculates where the sprite goes
				wall.right = column_index * 64
				wall.top = (7 - row_index) * 64

				# Adds the sprite to the list
				self.all_sprites_list.append(wall)
				self.wall_list.append(wall)

		self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, gravity_constant=GRAVITY)

	# Draws things
	def on_draw(self):
		# Begins to render the game at 60 frames per second
		# This means that it updates the frames 60 times per second, thus creating the illusion of moving objects
		arcade.start_render()

		# Draws all sprites
		self.all_sprites_list.draw()

	def on_key_press(self, key, modifiers):
		# Called whenever a key is pressed
		# Checks for which key is pressed
		if key == arcade.key.UP:
			# Checks if there is a platform beneath the character's feet.
			# You can't jump if you don't have a platform to jump from.
			if self.physics_engine.can_jump():
				self.player_sprite.change_y = JUMP_SPEED
		if key == arcade.key.LEFT:
			self.player_sprite.change_x = -MOVEMENT_SPEED
		if key == arcade.key.RIGHT:
			self.player_sprite.change_x = MOVEMENT_SPEED

	def on_key_release(self, key, modifiers):
		# Whenever the a key is released
		if key == arcade.key.LEFT or key == arcade.key.RIGHT:
			self.player_sprite.change_x = 0

	def update(self, delta_time):
		# Same as on_draw method. Renders at 60fps
		# Separate function because here I will cover the movement and game logic

		# Updates all of the sprites
		self.physics_engine.update()

		# View port stuff here

		# Checks if view port needs to be changed or not
		changed = False

		# Scroll left
		left_bndry = self.view_left + VIEWPORT_MARGIN
		if self.player_sprite.left < left_bndry:
			self.view_left -= left_bndry - self.player_sprite.left
			changed = True

		# Scroll right
		right_bndry = self.view_left + SCREEN_WIDTH - RIGHT_MARGIN
		if self.player_sprite.right > right_bndry:
			self.view_left += self.player_sprite.right - right_bndry
			changed = True

		# Scroll up
		top_bndry = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
		if self.player_sprite.top > top_bndry:
			self.view_bottom += self.player_sprite.top - top_bndry
			changed = True

		# Scroll down
		bottom_bndry = self.view_bottom + VIEWPORT_MARGIN
		if self.player_sprite.bottom < bottom_bndry:
			self.view_bottom -= bottom_bndry - self.player_sprite.bottom
			changed = True

		# If we need to scroll, go ahead and do it.
		if changed:
			arcade.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left, self.view_bottom, SCREEN_HEIGHT + self.view_bottom)


# The main function which runs the game
def main():
	window = Game()
	# Runs the setup method before anything else
	window.setup()
	arcade.run()


# If this is the main file, run main()
if __name__ == "__main__":
	main()

"""
This is used due to python being able to import variables and things from other python files and this just
checks to make sure that this is the main file
"""
