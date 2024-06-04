#!/usr/bin/env python3
# by Borys Łangowicz (neloduka_sobe)
from Evolution import Evolution
from PIL import Image
import numpy as np

def generate_copy_and_difference(index):
    evo_copy = evo.copy()
    evo_copy.mutate()
    difference = evo.calculate_difference(evo_copy)
    return evo_copy, difference

if __name__ == "__main__":
    PATH_TO_IMAGE = "image.png"
    PATH_TO_SPRITE = "sprite.png"
    NUM_OF_ITER = 10000
    NUM_IN_EPOCH = 100

    # Vectorize generate_copy_and_difference
    vectorized_function = np.vectorize(generate_copy_and_difference, otypes=[object, float])

    # Load the images
    image = Image.open(PATH_TO_IMAGE)
    sprite = Image.open(PATH_TO_SPRITE)

    # Initialize the class
    evo = Evolution(sprite, image)

    # Evolve
    for i in range(NUM_OF_ITER):
        results = np.empty((num_in_epoch, 2), dtype=object)
        copies, differences = vectorized_function(np.arange(NUM_IN_EPOCH))
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
