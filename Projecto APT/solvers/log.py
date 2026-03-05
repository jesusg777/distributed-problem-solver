import logging
import os

if not os.path.exists("files"):
    os.makedirs("files") 

logging.basicConfig(
    filename="files/problemstatus.log",
    filemode='a',
    format='%(asctime)s- %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)

""" logging.debug("This is a debug message")
logging.info("This is an info message")
logging.warning("This is a warning message")
 """