from skimage.color import lab2rgb
import numpy as np
# Define your RGB values
#rgb_values = [246,237,228]
#rgb_values = [value / 255 for value in rgb_values]  # List comprehension for division
# Convert RGB to LAB
#lab_values = color.rgb2lab([rgb_values], illuminant='D65', observer='2')
# Access the L, A, and B values
#lightness = lab_values[0][0]
#green_red = lab_values[0][1]
#blue_yellow = lab_values[0][2]

#print(f"LAB values: Lightness = {lightness:.2f}, A = {green_red:.2f}, B = {blue_yellow:.2f}")
lab = [93.89, 1.5, 5.43]
rgb = np.round(lab2rgb(lab)*255,0)
print(rgb[1])