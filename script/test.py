import sys 
import img_utils as iu

input_dir = sys.argv[1]

input_imgs = iu.load_imgs(input_dir)

iu.show_imgs(input_imgs)