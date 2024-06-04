#!/usr/bin/env python3
# by Borys Łangowicz (neloduka_sobe)
import numpy as np
import os
import copy

class Evolution:

    def init_matrix(self):

        self.dna = np.zeros((7, self.num_of_sprites))
        self.dna[0:3, :] = np.random.randint(0, 256, size=(3, self.num_of_sprites))
        self.dna[3, :] = np.random.randint(0, self.width + 1, size=self.num_of_sprites)
        self.dna[4, :] = np.random.randint(0, self.height + 1, size=self.num_of_sprites)
        self.dna[5, :] = np.random.uniform(0, self.size_factor, size=self.num_of_sprites)
        self.dna[6, :] = np.random.randint(0, 361, size=self.num_of_sprites)


    def __init__(self, sprite, goal_image, num_of_sprites=50):
        self.goal_image = goal_image
        self.width, self.height = self.goal_image.size
        self.sprite = sprite
        self.num_of_sprites = num_of_sprites
        self.size_factor = 1.5 # Change it later TODO
        self.init_matrix()
        

    def generate_image(self):
        #TODO
        # Generate image based on DNA
        pass

    def mutate(self, n=1):
        random_columns = np.random.choice(num_of_sprites, n, replace=False)
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
        difference = np.abs(np_goal.astype(np.int32) - np_current.astype(np.int32))
        return difference

    def save_step(self, step, directory="./steps"):
        filename = f"step{step}.PNG"
        path = os.path.join(directory, filename)
        self.save(path)

    def save(self, path):
        result = self.generate_image()
        reslut.save(path, format='PNG')
