#!/usr/bin/env python3
# by Borys Łangowicz (neloduka_sobe)
from Evolution import Evolution
from PIL import Image
import numpy as np

if __name__ == "__main__":
    PATH_TO_IMAGE = "image.png"
    PATH_TO_SPRITE = "sprite.png"
    NUM_OF_ITER = 10000

    # Load the images
    image = Image.open(PATH_TO_IMAGE)
    sprite = Image.open(PATH_TO_SPRITE)

    # Initialize the class
    evo = Evolution(sprite, image)

    # Evolve
    for i in range(NUM_OF_ITER):
        evo.evolve()
        if not i % 100:
            evo.save_step(i)
            print(f"Step: {i}; Saving to file: step{i}.PNG")

    evo.save("final.png")
