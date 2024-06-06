#!/usr/bin/env python3
# by Borys Łangowicz (neloduka_sobe)
from Evolution import Evolution
from PIL import Image
import numpy as np

def generate_copy_and_difference(index):
    global i
    evo_copy = evo.copy()
    evo_copy.mutate() 
    difference = evo_copy.calculate_difference()
    return evo_copy, difference

if __name__ == "__main__":
    PATH_TO_IMAGE = "image.png"
    PATH_TO_SPRITE = "sprite.png"
    NUM_IN_EPOCH = 100
    NUM_OF_SPRITES = 10000

    # Vectorize generate_copy_and_difference
    vectorized_function = np.vectorize(generate_copy_and_difference, otypes=[object, float])

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
    evo = Evolution(sprite, image, False, NUM_OF_SPRITES)

    try:
        # Evolve
        global i 
        i= 1
        positive_diff = 0
        while True:

            results = np.empty((NUM_IN_EPOCH, 2), dtype=object)
            copies, differences = vectorized_function(np.arange(NUM_IN_EPOCH))

            results[:, 0] = copies
            results[:, 1] = differences
            min_index = np.argmin(results[:, 1])
            new_object = results[min_index, 0]

            diff = results[min_index, 1] - evo.calculate_difference() 
            print(diff)
            if diff < 0:
                evo = new_object
                positive_diff = 0
            else:
                positive_diff += 1 

            # Save every 100 steps
            if not i % 100:
                evo.save_step(i)
                print(f"Step: {i}; Saving to file: step{i}.PNG")
                

            if positive_diff >= 35:
                print("Adding sprite!")
                evo.add_sprite()
                positive_diff = 0

            i += 1

    except KeyboardInterrupt:
        print(f"Saving image file in final.png")
        evo.save("final.png")
        print(f"Saving DNA in DNA.csv")
        evo.save_dna("DNA.csv")
        print(f"Exiting on iteration {i}!")
