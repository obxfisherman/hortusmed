import os

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')
image_dir =  os.path.join(main_dir, 'image')
asset_dir = os.path.join(main_dir, 'assets')

SCRN_SIZE=(600, 600)

clr_background=(217,189,124)	#yellowish, blends w the paper background image
clr_BLACK=(0,0,0)