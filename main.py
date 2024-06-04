#!/usr/bin/env python3
# by Borys Łangowicz (neloduka_sobe)
from Evolution import Evolution
from PIL import Image
import numpy as np

#TODO vectorize
def generate_copy_and_difference(evo):
    evo_copy = evo.copy()
    evo_copy.mutate()
    difference = evo_copy.calculate_difference()
    return evo_copy, difference

if __name__ == "__main__":
    PATH_TO_IMAGE = "image.png"
    PATH_TO_SPRITE = "sprite.png"
    NUM_OF_ITER = 10000
    NUM_IN_EPOCH = 1

    # Load the images
    image = Image.open(PATH_TO_IMAGE)
    sprite = Image.open(PATH_TO_SPRITE)

    # Resize the sprite
    w, h = image.size
    w //= 10
    h //= 10
    aspect_ratio = w / h
    if aspect_ratio > 1:
        h = int(w / aspect_ratio)
    else:
        w = int(h * aspect_ratio)

    sprite = sprite.resize((w, h))

    # Initialize the class
    evo = Evolution(sprite, image)

    # Evolve
    for i in range(NUM_OF_ITER):
        results = np.empty((NUM_IN_EPOCH, 2), dtype=object)

        copies = []
        differences = []

        # TODO vectorize
        for _ in range(NUM_IN_EPOCH):
            copy, difference = generate_copy_and_difference(evo)
            copies.append(copy)
            differences.append(difference)

        copies = np.array(copies)
        differences = np.array(differences)

        results[:, 0] = copies
        results[:, 1] = differences
        min_index = np.argmin(results[:, 1])
        new_object = results[min_index, 0]
        evo = new_object

        # Save every 100 steps
        if not i % 100:
            evo.save_step(i)
            print(f"Step: {i}; Saving to file: step{i}.PNG")

    evo.save("final.png")
