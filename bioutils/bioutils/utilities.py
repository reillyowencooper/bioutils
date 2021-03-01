import os, subprocess



def check_filepath_exists(filepath):
    pass

def remove_extension(filepath):
    fname = os.path.splitext(os.path.basename(filepath))[0]
    return fname