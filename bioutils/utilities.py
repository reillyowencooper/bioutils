import os, subprocess, gzip, shutil
from pathlib import Path

def create_directory(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)

def retrieve_basename(filepath):
    """Gets file basename without extension
    
    Args:
        filepath (str): Path to input file
    
    Returns:
        bname (str): Base filename without extension
    """
    bname = Path(filepath).stem
    return bname

def retrieve_extension(filepath):
    """Gets file extension without basename
    
    Args:
        filepath (str): Path to input file
        
    Returns:
        ext (str): File extension
    """
    ext = Path(filepath).suffix
    return ext

def check_filepath_exists(filepath, pathtype):
    """Checks if a path exists
    
    Args:
        filepath (str): Path to input file
        
    Returns:
        Boolean: True if filepath exists or False if not
    """
    if Path(filepath).exists:
        return True
    else:
        return False

def unpack_file(filepath):
    """Unpacks .tar.gz and .gz archives
    
    Args:
        filepath (str): Path to archive
    """
    fname = retrieve_basename(filepath)
    if Path(filepath).suffix == ".tar.gz":
        try:
            shutil.unpack_archive(filepath, fname)
        except:
            pass
    elif Path(filepath).suffix == ".gz":
        try:
            with gzip.open(filepath, 'rb') as inf:
                with open(fname, 'wb') as outf:
                    shutil.copyfileobj(inf, outf)
        except:
            pass
