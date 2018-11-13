import numpy as np
import BeautifulSoup

import argparse
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--pokemon-list", required=True,
                help="Path to where the raw Pokemon HTML file resides")
ap.add_argument("-s", "--sprites", required=True,
                help="Path where the sprites will be stored")
ap.add_argument("-c", "--coords",
                help="comma seperated list of source points")
args = vars(ap.parse_args())

soup = BeautifulSoup(open(args["pokemon_list"]).read())
pts = np.array(eval(args["coords"]), dtype="float32")
