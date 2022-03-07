import logging
from datetime import datetime
import os
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def Setup_Logger(name, log_file, level=logging.INFO):
    if(not os.path.exists('Logs')):
        os.mkdir('Logs')
    dt = datetime.now().strftime("%d %m %Y")
    handler = logging.FileHandler('Logs/' + dt + '_' + log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger