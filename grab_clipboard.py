import argparse
import clipboard
import console
import sys

parser = argparse.ArgumentParser()
parser.add_argument("clipboard")
parser.add_argument("append", nargs='?')
args = parser.parse_args()

if args.append is not None:
	new_clipboard = clipboard.get()
else:
	new_clipboard = ''

new_clipboard += args.clipboard

clipboard.set(new_clipboard)
console.alert('Clipboard set', new_clipboard, 'Yay', hide_cancel_button=True)
