from desktop_notifier import DesktopNotifier

notifier = DesktopNotifier()


def send_notification(message: str) -> None:
    """Sends a notification to desktop."""
    notifier.send_sync(title="Pulse", message=message)
