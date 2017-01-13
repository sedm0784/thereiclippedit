# Core imports
import argparse
import logging
import subprocess
import urllib

# Other imports
import pyperclip
import requests

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(levelname)s %(message)s')

pushover_max_url_length = 512
pushover_max_message_length = 1024
pushover_url = "https://api.pushover.net/1/messages.json"

# For the time-being, using a central API token. If There, I Clipped it becomes
# unexpectedly popular, I'll revisit.
pushover_api_token = "af28ycmcg5qi1hzch7jvvx1gdnzrgd"

supplementary_url_root = (
    'pythonista://grab_clipboard.py?action=run&argv={}')

append_url_suffix = '&argv=append'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("userkey", help="pushover user key")
    args = parser.parse_args()

    pushover_user_key = args.userkey

    cb = pyperclip.paste()

    payloads = []

    # Pushover maximum URL length is 512 characters. If the clipboard contents
    # are too long, we need to send multiple notifications, appending to the
    # existing contents for all notifications apart from the first.
    while cb:
        # Because of the URL encoding, we're not entirely sure what length of
        # message will fit. Just start with max possible, and then shrink until
        # it fits.
        message = cb

        argv = urllib.parse.quote(message)
        supplementary_url = supplementary_url_root.format(argv)

        # If this is not the first, tack on the "append" argv
        if payloads:
            supplementary_url += append_url_suffix

        url_length = len(supplementary_url)

        # If the URL is too long, shorten the message
        while url_length > pushover_max_url_length:
            overflow = url_length - pushover_max_url_length

            # Each character we remove from the message could be as many as 12
            # characters when URL encoded. (A four-byte utf-8 character
            # encodes to 4 groups of %xx.) This means if we are currently
            # over the limit and we remove overflow/12 characters, we'll
            # definitely still be over the limit.
            truncation_length = overflow // 12 + 1

            # Chop the characters off the end of the message
            removed = message[-truncation_length:]
            message = message[:-truncation_length]

            # And shrink the URL length accordingly
            url_length -= len(urllib.parse.quote(removed))

        if message != cb:
            # We had to chop some off the message. Update the URL
            argv = urllib.parse.quote(message)
            supplementary_url = supplementary_url_root.format(argv)

            if payloads:
                supplementary_url += append_url_suffix

        payloads.append((message, supplementary_url))
        cb = cb[len(message):]

    messages = len(payloads)
    for index, (message, supplementary_url) in enumerate(payloads):
        message_length = len(message)
        if message_length > pushover_max_message_length:
            logging.log(
                logging.ERROR,
                "Length of message ({}) exceeds Pushover maximum ({})".format(
                    message_length,
                    pushover_max_message_length))

        url_length = len(supplementary_url)
        if url_length > pushover_max_url_length:
            logging.log(
                logging.ERROR,
                "Length of supplementary URL ({}) exceeds Pushover maximum ({})".format(
                    url_length,
                    pushover_max_url_length))

        title = 'There, I Clipped It'

        if (index == 0):
            url_title = 'Slurp this into iOS clipboard'
        else:
            url_title = "Append this to iOS clipboard"

        if messages > 1:
            message_numbering = ' ({} of {})'.format(index + 1, messages)
            title += message_numbering
            url_title += message_numbering

        payload = {'token': pushover_api_token,
                'user': pushover_user_key,
                'title': title,
                'message': message,
                'url_title': url_title,
                'url': supplementary_url}

        r = requests.post(pushover_url, data=payload)

        if r.status_code != 200:
            logging.log(logging.ERROR, r.text)


def get_clipboard_data():
    p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    return p.communicate()[0]


if __name__ == '__main__':
    main()
