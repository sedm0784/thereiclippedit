import gntp.notifier
import sys
import os
import subprocess

def main():
    if len(sys.argv) != 2:
        sys.exit()

    # Get the path of the clipboard file.
    clipboard_path = sys.argv[1]

    if clipboard_path.find("clipboard") == -1:
        sys.exit()

    try:
        with open(clipboard_path) as f:
            cb = f.read()

            set_clipboard_data(bytes(cb, 'UTF-8'))

            try:
                growl = gntp.notifier.GrowlNotifier(
                        applicationName = "There, I Clipped It",
                        notifications = ["clipboardreceived"],
                        defaultNotifications = ["clipboardreceived"],
                )
                growl.register()

                # Send one message
                growl.notify(
                        noteType = "clipboardreceived",
                        title = "Clipboard Received",
                        description = cb,
                        sticky = False,
                        priority = 1,
                )
            except:
                # Just ignore exceptions. Maybe Growl isn't installed. Either
                # way, the notifications aren't important.
                pass

        os.remove(clipboard_path)

    except FileNotFoundError:
        pass


def set_clipboard_data(data):
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    p.communicate(data)

if __name__ == '__main__':
    main()
