#   Please be warned, that when turning on the "saving_enabled" feature, it will consume a lot of ram while it is saving
#   The frames. This is because every single frame that is played during the animation is recorded into the memory
#   At the moment, I dont see any other way to output a gif straight out of pygame. Increasing optimization_level alleviates
#   this to some extent
saving_enabled = False   # Record the animation
optimization_level = 1   # Every Nth frame to record while saving_enabled = True
duration = 8             # Pillow says this is duration of each frame in millisecond in the output gif but its weird

display_stats = True     # Display stats like pixels drawn, fps
display_grid = False     # displays a grid of tilesize x tilesize
silhouette = False       # Shows original position while animating (can get laggy)
brush_size = 3           # Default size of the brush

res = (800, 600)         # window size
tile_size = 5            # size of each tile, as well as the size of grid if enabled
lerp_speed = 0.05        # How fast should pieces assemble together. 0.01 = 1% of the distance covered per frame
output_name = "out"      # Name of the GIF generated if saving_enabled = True. (Do not include file extension!)

colors = [              # Edit these values to change or add more colors
    (255, 0, 0),        # red
    (0, 255, 0),        # green
    (0, 0, 255),        # blue
    (170, 0, 210),      # magenta
    (0, 130, 200),      # cyan
    (255, 128, 128),    # pale_red
    (255, 255, 255),    # White
]
default_background_color = (80, 80, 80)   # Default canvas background color
