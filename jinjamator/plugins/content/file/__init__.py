import os
import logging
import requests
from jinjamator.plugins.content.file import ftp

log = logging.getLogger(__name__)
py_open = open


def save(data, target_path, **kwargs):
    """save text data to a local file

    :param data: Data which should be written to a file
    :type data: str
    :param target_path: path to the new file
    :type target_path: str
    :return: Returns True on success, False on Failure
    :rtype: bool

    :Keyword Arguments:
        * *overwrite* (``bool``) --
          Should a existing file be overwritten?, defaults to True
    """
    mode = kwargs.get("mode", "w")
    if (not os.path.exists(target_path)) or (
        kwargs.get("overwrite", True) and os.path.isfile(target_path)
    ):
        with open(target_path, mode) as fh:
            fh.write(data)
            log.debug(f"successfully written file {target_path}")
        return True
    log.error(
        f"Path {target_path} exists and overwrite is not true or path is a directory"
    )
    return False


def load(path, **kwargs):
    """Load data from a textfile. This function works for local paths an http/https hosted files.

    :param path: Can be a local path or a http/https URL. For relative paths the current task base directory is set as basepath so test.txt will become /path/to/task/test.txt
    :type path: ``str``
    :return: On error opening the File `False` is returned. On success the content of the textfile is returned. 
    :rtype: ``bool`` or  ``str``

    :Keyword Arguments:
        None at the moment.
    """
    mode = kwargs.get("mode", "r")
    if not path.startswith("/"):
        path = f"{_jinjamator.task_base_dir}{os.path.sep}{path}"
    with open(path, mode) as fh:
        return fh.read()
    log.error(f"Path {path} does not exist")
    return False


def open(url, flags="r"):
    """Opens files from local filesystem or http/https/ftp and returns a corresponding descriptor

    :param url: URL
    :type url: ``str``
    :param flags: flags that should be passed to python open see https://docs.python.org/3/library/functions.html#open , defaults to "r"
    :type flags: ``str``, optional
    :return: File descriptor to local file or file served via http/https
    :rtype: ``file``
    """
    """
    
    """
    if url.startswith("http"):
        r = requests.get(url, stream=True, verify=False)
        return r.raw
    if url.startswith("ftp"):
        return ftp.open(url, flags)
    else:
        return py_open(url, flags)
