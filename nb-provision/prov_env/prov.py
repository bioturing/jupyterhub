import subprocess
import json
import os

from threading import Thread
import tempfile
from loguru import logger

import hashlib

def env_sha1_hashing(envfile):
    sha1 = hashlib.sha1()
    with open(envfile, 'rb') as f:
        while True:
            data = f.read()
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()

def python_kernel_naming(envname):
    return f"pykernel-{envname}".lower() # mustbe lowercase

def async_stream_process_stdout(process, log_func):
    """ Stream the stdout and stderr for a process out to display async https://andrewjorgensen.com/post/a-tale-of-two-pipes/
    :param process: the process to stream the log for
    :param log_func: a function that will be called for each log line
    :return: None
    """
    logging_thread = Thread(target=stream_process_stdout,
                            args=(process, log_func, ))
    logging_thread.start()

    return logging_thread

def stream_process_stdout(process, log_func):
    """ Stream the stdout and stderr for a process out to display https://andrewjorgensen.com/post/a-tale-of-two-pipes/
    :param process: the process to stream the logs for
    :param log_func: a function that will be called for each log line
    :return: None
    """
    while 1:
        line = process.stdout.readline()
        if not line:
            break

        log_func(line)

def log_fn(stdo):
    return lambda line: stdo.write(f"{line.decode('utf-8')}")

def async_stream_process_stdout_wrapper(ps, stdout_file, ps_name = ""):
    if stdout_file == None:
        stdout_file = os.path.join(tempfile.mkdtemp(), "stdout")
    with open(stdout_file, "w") as stdo:
        logger.info(f"Streamming stdout of process {ps_name}:{ps.pid} log to this file {stdout_file}")
        ps_logger = async_stream_process_stdout(ps, log_fn(stdo))
        ps_logger.join()

def create_conda_env(envfile, envname, stdout_file=None):
    if os.path.exists(f"/opt/conda/envs/{envname}"):
        logger.info(f"Environment {envname} exists")
        return True
    ps = subprocess.Popen(["mamba",
                            "env",
                            "create",
                            "-f",
                            f"{envfile}",
                            "--prefix",
                            f"/opt/conda/envs/{envname}" ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    async_stream_process_stdout_wrapper(ps, stdout_file, ps_name = "create_conda_env")
    ps.wait()
    return ps.returncode == 0


def install_kernelspec_python(envname, stdout_file=None):
    ps = subprocess.Popen([f"/opt/conda/envs/{envname}/bin/python",
                            "-m",
                            "ipykernel",
                            "install",
                            "--user",
                            "--name",
                            f"{python_kernel_naming(envname)}",
                            "--display-name",
                            f"{python_kernel_naming(envname)}" ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    async_stream_process_stdout_wrapper(ps, stdout_file, ps_name = "install_kernelspec_python")
    ps.wait()
    return ps.returncode == 0

def patching_kernelname_ipynb(nbfile, envname, lang="python"):
    if not nbfile.endswith(".ipynb"):
        print("Not a .ipynb file")
        return False
    nb = json.load(open(nbfile))
    try:
        kernelspec = nb["metadata"]["kernelspec"]
        kernelspec["display_name"] = python_kernel_naming(envname)
        kernelspec["name"] = python_kernel_naming(envname)
        kernelspec["language"] = lang
        nb["metadata"]["kernelspec"] = kernelspec
        with open(nbfile, 'w') as patched:
            json.dump(nb, patched)
    except Exception as ex:
        logger.warning(f"Patching kernel name error. Err: {repr(ex)}")
        return False
    finally:
        return True
    