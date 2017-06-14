from github import Github
import os
from PIL import Image
import requests
import math
from snakemake.utils import makedirs
import random


configfile: "config.yaml"

g = Github(config["token"])
training_repo = g.get_user("galaxyproject").get_repo("training-material")
creation_date = training_repo.created_at

rule all:
    input:
        contributors="images/contributors.png"

def extract_resizing_value(x, y, n):
    '''
    Extracting the resizing value using the algo in
    https://math.stackexchange.com/questions/466198/algorithm-to-get-the-maximum-size-of-n-squares-that-fit-into-a-rectangle-with-a

    x: width of the rectangle
    y: height of the rectangle
    n: number of square to fit in the (x,y) rectangle
    '''
    px = math.ceil(math.sqrt(n*x/y))
    py = math.ceil(math.sqrt(n*y/x))
    if math.floor(px*y/x)*px < n:
        sx = y/math.ceil(px*y/x)
    else:
        sx = x/px
    if math.floor(py*x/y)*py < n:
        sy = x/math.ceil(x*py/y)
    else:
        sy = y/py
    return math.floor(max(sx, sy))


rule extract_contributor_avatar:
    '''
    Create an image composed of the avatar of all the contributors
    '''
    output:
        contributors="images/contributors.png"
    run:
        avatar_paths = []
        avatar_dir = os.path.join("images", "avatars")
        makedirs(avatar_dir)
        # parse the contributors
        for contri in training_repo.get_contributors():
            # get the url to the avatar
            avatar_url = contri.avatar_url
            # download the avatar with requests
            avatar_path = os.path.join(avatar_dir, "%s.png" % contri.login)
            if not os.path.exists(avatar_path):
                r = requests.get(avatar_url, stream=True)
                r.raise_for_status()
                with open(avatar_path, "ab") as fd:
                    for chunk in r.iter_content(chunk_size=128):
                        fd.write(chunk)
            # add the path to the list of image paths
            avatar_paths.append(avatar_path)
        # create image to combine the avatars
        result = Image.new("RGB", (config["width"], config["height"]))
        # extract the resizing value
        img_nb = len(avatar_paths)
        print("img nb: %s" % img_nb)
        new_size = extract_resizing_value(
            config["width"],
            config["height"],
            img_nb)
        print("new size: %s" % new_size)
        # extract the number of row and number of column
        col_nb = math.floor(config["width"] / new_size)
        row_nb = math.floor(config["height"] / new_size)
        print("col: %s, row: %s" % (col_nb, row_nb))
        # compute extra pixels
        extra_left_right_pixels = config["width"] - col_nb*new_size
        extra_top_down_pixels = config["height"] - row_nb*new_size
        print("top-down: %s, left-right: %s" % (extra_top_down_pixels, extra_left_right_pixels))
        d_left = math.ceil(extra_left_right_pixels/2)
        d_top = math.ceil(extra_top_down_pixels/2)
        # find how many rectangles will be empty
        empty_rect_nb = col_nb*row_nb - img_nb
        # add as many empty path as many empty rectangles
        avatar_paths += [""] * empty_rect_nb
        # randomize the list of path
        random.shuffle(avatar_paths)
        # resize and add avatar
        for index, filename in enumerate(avatar_paths):
            # if empty path: add nothing
            if not os.path.exists(filename):
                continue
            # load and resize the image
            img = Image.open(filename)
            resized_img = img.resize((new_size, new_size))
            # extract the position of the image in the rectangle
            x = index // row_nb * new_size + d_left
            y = index % row_nb * new_size + d_top
            # add the image
            result.paste(resized_img, (x, y, x + new_size, y + new_size))
        # export the image
        result.save(str(output.contributors))