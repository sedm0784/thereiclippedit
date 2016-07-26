import argparse
import subprocess
import requests
import urllib

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("userkey", help="pushover user key")
    args = parser.parse_args()

    pushover_user_key = args.userkey # "uqDym6nBHZCFXvrwfGQSwE5ExPmR6o"

    # For the time-being, using a central API token. If There, I Clipped it becomes unexpectedly popular, I'll revisit.
    pushover_api_token = "af28ycmcg5qi1hzch7jvvx1gdnzrgd"
    #drafts_key = ""

    pushover_url = "https://api.pushover.net/1/messages.json"

    cb = get_clipboard_data()

    argv = urllib.parse.quote(cb)
    # Not 100% sure why we need to double-encode it, but we do. Something to do
    # with the way Pushover processes/presents supplementary URLs. (URLs in the
    # message body do not need to be double-encoded.
    argv = urllib.parse.quote(argv)

    payload = {'token': pushover_api_token,
            'user': pushover_user_key,
            'message': cb,
            'url_title': 'Slurp this into iOS clipboard',
            'url': 'pythonista://grab_clipboard.py?action=run&argv={}'.format(argv)}

            # This doesn't work. If we double encode, we get a URL encoded
            # string in the Draft, and if we don't, newlines are stripped. Why?
            #'url': 'drafts4://x-callback-url/create?key={0}&text={1}&action=Copy%20to%20Clipboard'.format(drafts_key, argv)}

    r = requests.post(pushover_url, data=payload)


def get_clipboard_data():
    p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    return p.communicate()[0]


if __name__ == '__main__':
    main()
