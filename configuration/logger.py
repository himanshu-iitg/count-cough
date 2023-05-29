import logging
import sys

root = logging.getLogger()

logformat = logging.Formatter(f'%(asctime)s %('f'name)s %(module)s, =>'
                                  f' %(lineno)d [%(levelname)s]: %(message)s')

# stream_handler = logging.StreamHandler(sys.stdout)
stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logformat)


file_handler = logging.FileHandler('flask.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logformat)

# sound_logger = logging.getLogger()
sound_logger = logging.getLogger('sound')
root.addHandler(stream_handler)
# sound_logger.addHandler(logging.StreamHandler())
