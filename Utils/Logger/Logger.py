import logging
from Utils.Logger.EnhancedRotatingFileHandler import EnhancedRotatingFileHandler
import os
from enum import IntEnum


class LogLevel(IntEnum):
    CRITICAL  = logging.CRITICAL  # = 50
    FATAL     = logging.CRITICAL  # = 50
    ERROR     = logging.ERROR     # = 40
    WARNING   = logging.WARNING   # = 30
    WARN      = logging.WARNING   # = 30
    INFO      = logging.INFO      # = 20
    DEBUG     = logging.DEBUG     # = 10
    NOTSET    = logging.NOTSET    # = 0


KB = 1024
MB = KB*KB


class RotatingFileInfo:
    def __init__(self, when, interval: int=1, maxBytes: int=(4*MB), backupCount: int=0):
        """
        This class defines the rules for rotating log files
        :param when:            'S' / 'M' / 'H' / 'D' / 'W0'...'W6'  for  Secs / Mins / Hours / Days / Weekday
        :param interval:        how many time-units before before file-rotation
        :param maxBytes:        maximum size of log file before rotating
        :param backupCount:     ZERO for no limits
        """
        self.when = when
        self.interval = interval
        self.maxBytes = maxBytes
        self.backupCount = backupCount


class LoggerSetup:
    def __init__(self, logger_name, log_file, log_dir = 'C:\\Logs',
                 log_level = LogLevel.DEBUG,
                 rotating_file_info = RotatingFileInfo('H', 1, 4*MB),
                 # log_line_format = '%(asctime)s.%(msecs)03d ~ %(name)s ~ %(levelname)s ~ %(message)s',
                 log_line_format = '%(asctime)s.%(msecs)03d ~ %(levelname)s ~ %(message)s',
                 encoding = None,
                 send_to_stdout = False):
        self.logger_name = logger_name
        self.log_file = log_file
        self.log_dir = log_dir
        self.log_level = int(log_level)
        self.rotating_file_info = rotating_file_info
        self.log_line_format = log_line_format
        self.encoding = encoding
        self.send_to_stdout = send_to_stdout


def get_loggerEx(logger_setup: LoggerSetup, append_target_file_to_logger_name: bool=False):
    #
    logger = logging.getLogger(logger_setup.logger_name)
    logger.setLevel(logger_setup.log_level)

    # ensure existence of target dir - default to 'C:\Logs' on failure
    try:
        if not os.path.exists(logger_setup.log_dir):
            os.makedirs(logger_setup.log_dir)
        log_dir = logger_setup.log_dir
    except OSError:
        log_dir = 'C:\\Logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

    log_path = os.path.join(log_dir, logger_setup.log_file)     # + '.log')

    fh = EnhancedRotatingFileHandler(log_path,
                                     when = logger_setup.rotating_file_info.when,
                                     interval = logger_setup.rotating_file_info.interval,
                                     maxBytes = logger_setup.rotating_file_info.maxBytes,
                                     backupCount = logger_setup.rotating_file_info.backupCount,
                                     encoding = logger_setup.encoding
                                     )

    fh.setLevel(logger_setup.log_level)     # default:  logging.DEBUG
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
    # formatter = logging.Formatter('%(asctime)s.%(msecs)03d ~ %(name)s ~ %(levelname)s ~ %(message)s')
    formatter = logging.Formatter(logger_setup.log_line_format)
    formatter.datefmt = "%Y-%m-%d %H:%M:%S"
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    if not append_target_file_to_logger_name:
        logger.handlers = []
    logger.addHandler(fh)
    if logger_setup.send_to_stdout:
        if not append_target_file_to_logger_name:
            logger.addHandler(ch)   # avoid appending multiple STDOUT handlers
    return logger
