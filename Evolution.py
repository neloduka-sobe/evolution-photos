#!/usr/bin/env python3
# by Borys Łangowicz (neloduka_sobe)
import numpy as np
import os
import copy
from PIL import Image, ImageDraw, ImageOps
from pathlib import Path

class Evolution:
    def __init__(self, sprite, goal_image, from_file = False, num_of_sprites=100):
        self.goal_image = goal_image
        self.width, self.height = self.goal_image.size
        self.goal_to_compare = np.array(self.goal_image).astype(np.int32)
        self.sprite = sprite
        self.sprite_width, self.sprite_height = self.sprite.size
        self.num_of_sprites = num_of_sprites
        self.size_factor = 5
        self.acc_num_of_sprites = 1

        if from_file:
            try:
                self.load_matrix(from_file)
            except FileNotFoundError as e:
                print(e)
                self.init_matrix()
        else:
            self.init_matrix()


    def init_matrix(self):
        # Initialize the DNA matrix with random values
        self.dna = np.zeros((8, self.num_of_sprites))
        self.dna[0:4, :] = np.random.randint(1, 256, size=(4, self.num_of_sprites))
        self.dna[4, :] = np.random.randint(0, self.width + 1, size=self.num_of_sprites)
        self.dna[5, :] = np.random.randint(0, self.height + 1, size=self.num_of_sprites)
        self.dna[6, :] = np.random.uniform(0.5, self.size_factor, size=self.num_of_sprites)
        self.dna[7, :] = np.random.randint(0, 361, size=self.num_of_sprites)


    def load_matrix(self, file):
        f = Path(file)
        if f.is_file() and f.exists():
            loaded_dna = np.loadtxt(file, delimiter=",")

            # Saving in proper datatypes
            self.dna = np.zeros((8, self.num_of_sprites))
            self.dna[0:4, :] = loaded_dna[0:4, :].astype(np.uint8)
            self.dna[4, :] = loaded_dna[4, :].astype(np.uint8)
            self.dna[5, :] = loaded_dna[5, :].astype(np.uint8)
            self.dna[6, :] = loaded_dna[6, :].astype(np.float32)
            self.dna[7, :] = loaded_dna[7, :].astype(np.uint8)
        else:
            raise FileNotFoundError("No file")


    def generate_image(self):
        # Generate image based on DNA
        canvas = Image.new('RGB', (self.width, self.height), (255, 255, 255))

        for i in range(self.acc_num_of_sprites):
            red = int(self.dna[0, i])
            green = int(self.dna[1, i])
            blue = int(self.dna[2, i])
            transparency = int(self.dna[3, i])
            x = int(self.dna[4, i])
            y = int(self.dna[5, i])
            size_factor = self.dna[6, i]
            rotation = int(self.dna[7, i])

            # Resize
            sprite_width = int(self.sprite_width * size_factor)
            sprite_height = int(self.sprite_height * size_factor)
            sprite = self.sprite.resize((sprite_width, sprite_height), Image.ANTIALIAS)
            # Change the sprite color by blending with a color overlay
            color_overlay = Image.new('RGBA', sprite.size, (red, green, blue, transparency))
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
        n = max(1, int(self.acc_num_of_sprites*0.15))

        # Always include last added sprite
        random_columns = np.append(np.random.choice(self.acc_num_of_sprites, n, replace=False), self.acc_num_of_sprites)

        for col in random_columns:
            # Add small perturbations to the existing values
            self.dna[0:4, col] += np.random.randint(-10, 11, size=4)
            self.dna[0:4, col] = np.clip(self.dna[0:4, col], 0, 255)  # Ensure values stay within 0-255 range

            self.dna[4, col] += np.random.randint(-10, 11)
            self.dna[4, col] = np.clip(self.dna[4, col], 0, self.width)  # Ensure values stay within 0-width range

            self.dna[5, col] += np.random.randint(-10, 11)
            self.dna[5, col] = np.clip(self.dna[5, col], 0, self.height)  # Ensure values stay within 0-height range

            self.dna[6, col] += np.random.uniform(-0.1, 0.1)
            self.dna[6, col] = np.clip(self.dna[6, col], 0.5, self.size_factor)  # Ensure values stay within 0.5-size_factor range

            self.dna[7, col] += np.random.randint(-10, 11)
            self.dna[7, col] = np.mod(self.dna[7, col], 361)  # Ensure values stay within 0-360 degrees range


    def add_sprite(self):
        # Increment the number of active sprites
        if self.acc_num_of_sprites < self.num_of_sprites:
            self.acc_num_of_sprites += 1

    def copy(self):
        return copy.deepcopy(self)

    def calculate_difference(self):
        np_current = np.array(self.generate_image())

        # Calculate the difference
        difference = np.sum(np.abs(self.goal_to_compare - np_current.astype(np.int32)))
        return difference


    def save_step(self, step, directory="./steps"):
        # Save the current image
        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = f"step{step}.PNG"
        path = os.path.join(directory, filename)
        self.save(path)

    def save(self, path):
        # Save the image to a file
        result = self.generate_image()
        result.save(path, format='PNG')

    def save_dna(self, filename):
        # Save the DNA matrix to file
        np.savetxt(filename, self.dna, delimiter=",")
