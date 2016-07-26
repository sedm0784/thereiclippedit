#!/usr/bin/env python3

import argparse
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(levelname)s %(message)s')

push_script_name = "push_clipboard.py"
pull_script_name = "pull_clipboard.py"

def main():
    parser = argparse.ArgumentParser(description="Installs the various component parts of the There, I Clipped It tool.", epilog="N.B. The installer bakes the location of the python used to run it into the installed components, so if you want There I Clipped It to use a virtualenv, be sure to activate your virtualenv before running this script.")
    parser.add_argument("-u", "--userkey", required=True, help="Pushover user key. You can find this near the top of the page: https://pushover.net/ (when logged in).")
    parser.add_argument("-c", "--computername", required=True, help="Name of this computer. This needs to match the value used in the List action in the Push Clipboard Workflow on your iOS device.")
    args = parser.parse_args()

    # Get path of python
    python_path = sys.executable

    # Get path of directory containing this script (for path of scripts and
    # sharedboards folder)
    install_path = os.path.dirname(os.path.realpath(__file__))

    # Install requirements
    requirements_path = os.path.join(install_path, "requirements.txt")
    call_command("pip install -r {}".format(requirements_path))

    watch_path = os.path.join(install_path, "sharedboards")
    clipboard_path = os.path.join(watch_path, "clipboard-{}.txt".format(args.computername))

    if sys.platform == "darwin":
        install_osx(args, install_path, watch_path, clipboard_path, python_path)
    elif sys.platform == "win32":
        install_windows(args, install_path, clipboard_path)


def install_osx(args, install_path, watch_path, clipboard_path, python_path):
    # Install launchd plist
    # Copy into location, editing variables as we go
    launchagents_path = os.path.expanduser("~/Library/LaunchAgents")
    launchd_plist_source_path = "uk.co.whileyouweregone.thereiclippedit.plist"
    launchd_plist_destination_path = os.path.join(launchagents_path, launchd_plist_source_path)
    launchd_replacements = (
        ("%%PYTHON_PATH%%", python_path),
        ("%%PULL_SCRIPT_PATH%%", os.path.join(install_path, pull_script_name)),
        ("%%CLIPBOARD_PATH%%", clipboard_path),
        ("%%WATCH_PATH%%", watch_path))

    fill_in_placeholders(os.path.join(install_path, launchd_plist_source_path), launchd_replacements, launchd_plist_destination_path)

    # Switch on watch folder
    call_command("launchctl load {}".format(launchd_plist_destination_path))

    # Install Service
    # Copy whole folder
    workflow_template_path = os.path.join(install_path, "template_ThereIClippedIt.workflow")
    workflow_path = os.path.join(install_path, "ThereIClippedIt.workflow")
    shutil.copytree(workflow_template_path, workflow_path)

    # Fill in variables in place
    workflow_replacements = (
        ("%%PYTHON_PATH%%", python_path),
        ("%%PUSH_SCRIPT_PATH%%", os.path.join(install_path, push_script_name)),
        ("%%USER_KEY%%", args.userkey))
    fill_in_placeholders(os.path.join(workflow_path, "Contents/document.wflow"), workflow_replacements)

    # Install clipboard service
    call_command("open {}".format(workflow_path))

    # Remind user to set up keyboard shortcut
    print(
        "There, I Clipped It has been installed. Don't forget to set up a\n"
        "keyboard shortcut to the There, I Clipped It Service in:\n\n"
        "    System Preferences -> Keyboard -> Shortcuts -> Services")


def install_windows(args, install_path, clipboard_path):
    # Create VBS push script
    push_vbs_template_path = os.path.join(install_path, "template_create_push_shortcut.vbs")
    push_vbs_path = os.path.join(install_path, "create_push_shortcut.vbs")
    push_replacements = (
            ("%%PUSH_SCRIPT_PATH%%", os.path.join(install_path, push_script_name)),
            ("%%USER_KEY%%", args.userkey))

    fill_in_placeholders(push_vbs_template_path, push_replacements, push_vbs_path)

    # Create VBS pull script
    pull_vbs_template_path = os.path.join(install_path, "template_create_pull_shortcut.vbs")
    pull_vbs_path = os.path.join(install_path, "create_pull_shortcut.vbs")
    pull_replacements = (
            ("%%PULL_SCRIPT_PATH%%", os.path.join(install_path, pull_script_name)),
            ("%%CLIPBOARD_PATH%%", clipboard_path))

    fill_in_placeholders(pull_vbs_template_path, pull_replacements, pull_vbs_path)

    # Install them
    call_command("cscript {}".format(push_vbs_path))
    call_command("cscript {}".format(pull_vbs_path))

    # Delete them
    os.remove(push_vbs_path)
    os.remove(pull_vbs_path)


def fill_in_placeholders(source_path, replacements, output_path=None):
    logging.log(logging.INFO, "fill_in_placeholders       source: {}".format(source_path))
    logging.log(logging.INFO, "fill_in_placeholders       output: {}".format(output_path))
    logging.log(logging.INFO, "fill_in_placeholders replacements: {}".format(replacements))

    if output_path is None:
        output_path = source_path

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        with open(source_path) as src_file:
            for line in src_file:
                for placeholder, replacement in replacements:
                    line = line.replace(placeholder, replacement)
                tmp_file.write(line)

    shutil.copystat(source_path, tmp_file.name)
    shutil.move(tmp_file.name, output_path)


def call_command(command):
    process = subprocess.Popen(command.split(' '),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    return process.communicate()


if __name__ == "__main__":
    main()
