import os
import logging
from os.path import join, dirname
from dotenv import load_dotenv

formatter = '%(levelname)s : %(asctime)s : %(message)s'
logging.basicConfig(level=logging.INFO, format=formatter)

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")