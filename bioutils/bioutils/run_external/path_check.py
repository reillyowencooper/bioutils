from distutils.spawn import find_executable
import os

def path_check(tool, user_path = None):
    """Checks if tool is on path

    Args:
        tool (str): Name of tool executable (e.g., mmseqs, hmmsearch)
        user_path (str, optional): User-specified environment path. Defaults to None, which is the global Path.

    Returns:
        Boolean : True if tool on path, else False
    """
    if user_path is None:
        user_path = os.environ['PATH']
    if find_executable(tool, path = user_path) is not None:
        return True
    else:
        print(tool + ' cannot be found on ' + user_path)
        return False

def multiple_path_check(tools, user_path = None):
    """For a list of tools, checks if on path

    Args:
        tools (list): List of all tools to check
        user_path (str, optional): User-specified environment path. Defaults to None, which is the global Path.

    Returns:
        Boolean : True if every tool is on path, else False. Will print tools it can't find to console
    """
    if user_path is None:
        user_path = os.environ['PATH']
    for tool in tools:
        if not path_check(tool, path = user_path):
            return False
    return True