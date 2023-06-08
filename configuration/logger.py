import logging
import sys
format_string = f'%(asctime)s %('f'name)s %(module)s, =>' \
                f' %(lineno)d [%(levelname)s]: %(message)s'

logformat = logging.Formatter(format_string)

logging.basicConfig(format=format_string)

stream_handler = logging.StreamHandler(sys.stdout)
# stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logformat)


# file_handler = logging.FileHandler('flask.log')
# file_handler.setLevel(logging.DEBUG)
# file_handler.setFormatter(logformat)

# sound_logger = logging.getLogger()
sound_logger = logging.getLogger('sound')
sound_logger.propagate = False
sound_logger.setLevel(logging.DEBUG)
# sound_logger.handlers.clear()
sound_logger.addHandler(stream_handler)
# sound_logger.addHandler(file_handler)

# root.addHandler(stream_handler)
# sound_logger.addHandler(logging.StreamHandler())
