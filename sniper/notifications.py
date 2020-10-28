import sys
import threading
import logging
import asyncio
try:
    import apprise
except Exception:
    logging.error(
        'Could not import all required modules. '\
        'Please run the following command again:\n\n'\
        '\tpipenv install\n')
    exit()


class Notifier():
    def __init__(self, notification_config, notification_queue, target_gpu):
        self.config = notification_config
        self.notifications = notification_config['notifications']
        self.queue = notification_queue
        self.gpu = target_gpu
        if sys.platform == 'win32' and sys.version_info >= (3, 8, 0):
            asyncio.set_event_loop_policy(
                asyncio.WindowsSelectorEventLoopPolicy())

    def send_notifications(self, notification_type):
        for name, service in self.config['services'].items():
            logging.info(f'Sending {notification_type} notification to {name}...')
            apobj = apprise.Apprise()
            apobj.add(service['url'])
            title = f"{notification_type.replace('-',' ').title()} - {self.gpu['name']}"
            msg = self.notifications[notification_type]['message']
            if service['screenshot']:
                apobj.notify(title=title, body=msg,
                             attach='screenshot.png')
            else:
                apobj.notify(title=title, body=msg)

    def worker(self):
        while True:
            notification_type = self.queue.get()
            self.send_notifications(notification_type)
            self.queue.task_done()

    def start_worker(self):
        threading.Thread(target=self.worker, daemon=True).start()
