# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                          api.log.logging_format.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
import logging
# |--------------------------------------------------------------------------------------------------------------------|

# Create logger
logger = logging.getLogger("IOLOG")
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - [%(microservice)s <-> %(clientip)s] - C_ID: %(chat_id)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

