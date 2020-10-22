saving_enabled = False   # Record the animation
optimization_level = 1   # Every Nth frame to record while saving_enabled = True
duration = 8            # Pillow says this is duration of each frame in millisecond in the output gif but its weird

display_stats = True     # Display stats like pixels drawn, fps
display_grid = False     # displays a grid of tilesize x tilesize
silhouette = False       # Shows original position while animating (can get laggy)
brush_size = 3           # Default size of the brush

res = (800, 600)         # window size
tile_size = 8            # size of each tile, as well as the size of grid if enabled
lerp_speed = 0.05         # How fast should pieces assemble together. 0.01 = 1% of the distance covered per frame
output_name = "out2"      # Name of the GIF generated if saving_enabled = True. (Do not include file extension!)
