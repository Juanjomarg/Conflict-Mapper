from python_files.functions import *
from python_files.libraries import *
from python_files.RSS_puller_parser import *


files=os.listdir("./assets/RSS/RAW/XML/")

parse_all_rss(files)