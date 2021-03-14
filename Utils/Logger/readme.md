# Enhanced LOGGER


<img src = "imagesForWiki/logger_logo.jpg" width="100%" heigth="300"/>


This module:
 1. Enhances python's standard logger . . . (creates the destination folder if it doesn't already exist).
 2. Combines file-size and time-frame constraints . . . (whichever comes first since last file rotation).
 3. Simplifies and clarifies logger initialization.

In order to use the logger please supply an instance of <b><u>LoggerSetup</u></b> class as shown below.

## Usage Example:
```python
from Logger.Logger import *


def get_scenario_execution_logger(logger_name: str, log_file: str, log_dir: str, append_target_file_to_logger_name: bool=False):
    #                          logger_name=logger_name, log_file="scenario_execution_events_log.log", log_dir=scenario_execution_results_dir,
    logger_setup = LoggerSetup(logger_name=logger_name, log_file=log_file, log_dir=log_dir,
                               log_level=LogLevel.DEBUG,
                               # rotating_file_info=RotatingFileInfo(when='S', interval=7, maxBytes=50*KB),     # replace log file once every 7 sec     (or 7 seconds have passed)
                               # rotating_file_info=RotatingFileInfo(when='M', interval=1, maxBytes=50*KB),     # replace log file upon reaching 50 KB  (or 1 minute has passed)
                               rotating_file_info=RotatingFileInfo(when='H', interval=1, maxBytes=1*MB),        # replace log file upon reaching 1 MB   (or 1 hour has passed)
                               # log_line_format = '%(asctime)s.%(msecs)03d ~ %(name)s ~ %(levelname)s ~ %(message)s'
                               log_line_format = '%(asctime)s.%(msecs)03d ~ %(levelname)s ~ %(message)s',
                               send_to_stdout=True
                               )
    logger = get_loggerEx(logger_setup, append_target_file_to_logger_name=append_target_file_to_logger_name)
    return logger

# single-file association with *logger name* (each setup of a *logger by name* re-defines the output file)
dir1 = 'C:\\TEMP\\Logs1'
dir2 = 'C:\\TEMP\\Logs2'
logger1 = get_scenario_execution_logger(logger_name='single file logger', log_file='log.log', log_dir=dir1)
logger1.info('Single-File RESULT :)')
logger1 = get_scenario_execution_logger(logger_name='single file logger', log_file='log.log', log_dir=dir2)
logger1.info('Single-File RESULT :)')

# multi-file association with *logger name* (second instantiation of *logger by name* appends another target log file for each write operation (info/error/debug...))
dir0 = 'C:\\TEMP\\Logs'
logger2 = get_scenario_execution_logger(logger_name='multi file logger', log_file='log1.log', log_dir=dir0)
logger2 = get_scenario_execution_logger(logger_name='multi file logger', log_file='log2.log', log_dir=dir0, append_target_file_to_logger_name=True)
logger2.info('Multi-File RESULT :)')
```


<img src = "imagesForWiki/logger_levels.png" width="100%" heigth="300"/>
.
