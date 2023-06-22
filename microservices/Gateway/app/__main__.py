# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                    app.__main__.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from resources.data import TELEGRAM_API

from services.telegram.get_message import Core
from services.controller.post_data import PostController

from connections.log import LogConnect

from threads.executable import Threads

from utils.process_monitor import ProcessMonitor
# |--------------------------------------------------------------------------------------------------------------------|

process_monitor: ProcessMonitor = ProcessMonitor()

# Start process monitoring
process_monitor.init_process_start()

core: Core = Core()
log_connect: LogConnect = LogConnect()
post_controller: PostController = PostController()
threads: Threads = Threads()

# Finish process monitoring
process_monitor.init_process_finish()

while True:
    process_monitor.clock_process_start()

    # Get the last received message
    last_message: dict[str, dict[str, str]] = core.last_message()

    # Start process monitoring for the clock process
    threads.start_thread(process_monitor.clock_process_finish, None, True)

    if last_message:
        # Process each received message
        for id_ in last_message.keys():
            data: int = last_message[id_]
            data["chat_id"] = str(id_)

            # Start a thread to report the message to the log
            log_connect.report("get", TELEGRAM_API['uri'], 'info', str(id_), True)

            # Start a thread to send the message
            threads.start_thread(post_controller.send, data)

            # Start process monitoring for the current message processing
            threads.start_thread(process_monitor.clock_process_finish, data['username'])
