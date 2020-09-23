import logging
import apprise

def send_notifications(target_gpu, notification_type, notifications):
    for name, service in notifications['services'].items():
        logging.info(f'Sending notifications to {name}')
        apobj = apprise.Apprise()
        apobj.add(service['url'])
        title = f"Alert - {target_gpu['name']} {notification_type}"
        msg = notifications[notification_type]['message']
        if service['screenshot']:
            apobj.notify(title=title, body=msg,
                         attach='screenshot.png')
        else:
            apobj.notify(title=title, body=msg)
