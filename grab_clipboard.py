import argparse
import clipboard
import console
import sys

parser = argparse.ArgumentParser()
parser.add_argument("clipboard")
args = parser.parse_args()

clipboard.set(args.clipboard)
console.alert('Clipboard set', args.clipboard, 'Yay', hide_cancel_button=True)
