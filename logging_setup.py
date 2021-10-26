import logging, sys

file_handler = logging.FileHandler(filename='tmp.log')
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]

FORMAT_STRING = "[%(asctime)s] {%(filename)s:%(lineno)d}\n%(levelname)s - %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=FORMAT_STRING,
    handlers=handlers
)

logger = logging.getLogger('LOGGER_NAME')

