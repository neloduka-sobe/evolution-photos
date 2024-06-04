#!/usr/bin/env python3
# by Borys Łangowicz (neloduka_sobe)
import numpy as np
import os
import copy
from PIL import Image, ImageDraw, ImageOps

class Evolution:

    def init_matrix(self):

        self.dna = np.zeros((7, self.num_of_sprites))
        self.dna[0:3, :] = np.random.randint(0, 256, size=(3, self.num_of_sprites))
        self.dna[3, :] = np.random.randint(0, self.width + 1, size=self.num_of_sprites)
        self.dna[4, :] = np.random.randint(0, self.height + 1, size=self.num_of_sprites)
        self.dna[5, :] = np.random.uniform(0.1, self.size_factor, size=self.num_of_sprites)
        self.dna[6, :] = np.random.randint(0, 361, size=self.num_of_sprites)


    def __init__(self, sprite, goal_image, num_of_sprites=50):
        self.goal_image = goal_image
        self.width, self.height = self.goal_image.size
        self.sprite = sprite
        self.sprite_width, self.sprite_height = self.sprite.size
        self.num_of_sprites = num_of_sprites
        self.size_factor = 5 # Change it later TODO
        self.num_of_sprites = 100 # Change it later TODO
        self.init_matrix()
        

    def generate_image(self):
        # Generate image based on DNA
        canvas = Image.new('RGB', (self.width, self.height), (255, 255, 255))

        for i in range(self.num_of_sprites):
            red = int(self.dna[0, i])
            green = int(self.dna[1, i])
            blue = int(self.dna[2, i])
            x = int(self.dna[3, i])
            y = int(self.dna[4, i])
            size_factor = self.dna[5, i]
            rotation = int(self.dna[6, i])

            # Resize
            sprite_width = int(self.sprite_width * size_factor)
            sprite_height = int(self.sprite_height * size_factor)
            if (sprite_height <= 0 or sprite_width <= 0):
                continue

            sprite = self.sprite.resize((sprite_width, sprite_height), Image.ANTIALIAS)
            # Change the sprite color by blending with a color overlay
            color_overlay = Image.new('RGBA', sprite.size, (red, green, blue, 255))
            sprite = Image.blend(sprite, color_overlay, alpha=0.5)

            # Rotate the sprite
            sprite = sprite.rotate(rotation, expand=True)

            # Calculate the top-left corner for pasting
            top_left_x = x - sprite.size[0] // 2
            top_left_y = y - sprite.size[1] // 2
            
            # Paste the sprite onto the canvas
            canvas.paste(sprite, (top_left_x, top_left_y), sprite)

        return canvas


    def mutate(self, n=1):
        random_columns = np.random.choice(self.num_of_sprites, n, replace=False)
        for col in random_columns:
            self.dna[0:3, col] = np.random.randint(0, 256, size=3) 
            self.dna[3, col] = np.random.randint(0, self.width + 1)
            self.dna[4, col] = np.random.randint(0, self.height + 1)
            self.dna[5, col] = np.random.uniform(0, self.size_factor)
            self.dna[6, col] = np.random.randint(0, 361)

    def copy(self):
        return copy.deepcopy(self)

    def calculate_difference(self):
        np_current = np.array(self.generate_image())
        np_goal = np.array(self.goal_image)

        # Calculate the difference
        difference = np.sum(np.abs(np_goal.astype(np.int32) - np_current.astype(np.int32)))
        return difference

    def save_step(self, step, directory="./steps"):
        filename = f"step{step}.PNG"
        path = os.path.join(directory, filename)
        self.save(path)

    def save(self, path):
        result = self.generate_image()
        result.save(path, format='PNG')
