#logger  sample.
import datetime
import logging
import sys
from logging.handlers import TimedRotatingFileHandler
import os
from time import sleep, time

logging.basicConfig(format='%(levelname)s:%(funcName)s:%(message)s', level = logging.DEBUG)
 
LOG_FILE = '/vault/dpo/logs/generate_label.log'
LOG_Folder = '/vault/dpo/logs/'
if not os.path.exists(LOG_Folder):
    os.makedirs(LOG_Folder)
# logging.basicConfig()
logging.root.setLevel(logging.NOTSET)

# Create a custom logger
logger = logging.getLogger(__name__)

# Setup Console Handler  
# c_handler = logging.StreamHandler(sys.stdout)
# c_handler.setLevel(logging.ERROR)
# c_handler.setFormatter(logging.Formatter('%(message)s'))

# Setup Log Handlers
f_handler = TimedRotatingFileHandler(LOG_FILE, when="M", interval=1,backupCount=3)
f_handler.suffix += ".log"
f_handler.setLevel(logging.WARNING)
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)

# Add handlers to the logger
# logger.addHandler(c_handler)
logger.addHandler(f_handler)

for i in range(1,300):
    sleep(2)
    logger.debug('em this is a debug message.'+ str(datetime.datetime.now()))
    logger.info('haha ha  , I am an information')
    logger.warning('N. I am warning......')
    logger.error('ooh , you find an error..' + str(datetime.datetime.now()))

 