import os, subprocess, gzip, shutil

def create_directory(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)

def check_filepath_exists(filepath):
    pass

def remove_extension(filepath):
    fname = os.path.splitext(os.path.basename(filepath))[0]
    return fname

def unpack_file(filepath):
    if filepath.endswith('.gz'):
        try:
            fname = os.path.splitext(os.path.basename(filepath))[0]
            with gzip.open(filepath, 'rb') as inf:
                with open(fname, 'wb') as outf:
                    shutil.copyfileobj(inf, outf)
                    os.remove(filepath)
            return fname
        except:
            pass
