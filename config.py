# the orientation of the hexagons. set 'flat' for flat, and 'pointy' for pointy
ORIENTATION = 'pointy'

# Background of the tiles. If you want background tiles,
# set this to a hex color string of a color matching your filament material.

# If you don't want to use background tiles for your print, setting this color
# to a similar color as your wallpaper on the wall you want to hang the print on would be recommended
BACKGROUND_COLOR = '#000000'

# This is the color of the triangle borders, so it should match the filament you want to use for printing the
# kumiko panels (brown-ish in my case)
TRIANGLE_BORDER_COLOR = '#683e07'

# Set to "True" if you want to exclude the background, and "False" if you want to keep it.
# What this mean in practice is if you have an image like the saturn provided one, and you include the background,
# then a lot of patterns will be generated for the black background. For that type of image I rather exclude it,
# so I set it to true.

# For images that don't have a background, and you want the entire image to generate patterns, then set this to False
EXCLUDE_BACKGROUND = True

# This value determines how many prominent colors should be extracted from the original image and used for the
# generation.

# For example, say you want to use 4 different filaments, and you also want to exclude the background. then setting
# the amount to 5 would make sense (as we will scrap the background color anyway, resulting in 4 total used colors).

# If you instead had wanted to include the background then setting 4 would make sense as we're not scrapping a color.
PROMINENT_COLOR_AMOUNT = 5

# These values are the ones you want to change to increase/decrease the resolution of the grid.

# You'll have to play with these values a bit depending on the size of your uploaded image.
# If it's a landscape image, keeping both the width and height more or less the same would make sense.
# If it's portrait or other aspects, you'll have to play around to make the image fit to the grid.

# Once you think the aspect ratio is right, you can start multiplying or increasing/decreasing the values depending
# on how large you want the entire panel.

# ex. 15 x 15 works for my landscape image, but I'd like to make it twice as big, I then set it to 30 x 30.
# this will mean it will have the same aspect ratio, but the size and resolution will improve.

# You'll have to estimate the size of the actual print yourself by counting triangles and measuring what your triangle
# size would be with your own prints.
GRID_WIDTH = 5
GRID_HEIGHT = 5

# This is the path to the input file you want to use. PNG should have full support, and I cannot promise other formats
# will work.
FILE_PATH = "input.png"
