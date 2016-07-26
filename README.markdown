# There, I Clipped It

## What *Is* This?

There, I Clipped It is an unholy amalgam of scripts, tools, and configuration
settings that make it FAST and EASY to INSTANTLY squirt your clipboard from your iOS
devices to your computers and vice versa.

I made it because it was fun to do, and in order to avoid having to be LOCKED
IN to any of the numerous professional solutions for this problem[^1].

It is named in homage to the [meme wherein repairs are made in an inelegant but
effective style](http://google.com/search?q=there+i+fixed+it). If There, I
Clipped It existed outside of your computing device, it would consist entirely
of gaffer tape and odd bits of cardboard.

## How Does It Work?

### Squirting the iOS clipboard to OS X

You invoke the There, I Clipped It workflow in the [Workflow
app](http://workflow.is/). It asks you which of your computers you want your
clipboard to be SQUIRTED to. It then saves the contents of your clipboard to a
file in your Dropbox. The corresponding computer, which is watching like a HAWK
for that file to be created (via
[launchd](https://en.wikipedia.org/wiki/Launchd)), then runs a Python script to
replace your clipboard with the file's contents.

### Squirting the OS X clipboard to iOS

You press a keyboard shortcut. (I'm using Command+Option+Ctrl+V). This invokes
the There, I Clipped It Service, which runs a Python script which reads your
clipboard and sends it to your iOS device as a push notification (via the
[Pushover app](http://pushover.net/)). When your iOS device pings, you open the
notification and tap on a link, which runs a script in the [Pythonista
app](http://omz-software.com/pythonista/) which replaces your iOS clipboard
with the copied text.

## Sounds Good; I Want It.

You really don't.

Whilst I use it on several computers, and it works, There, I Clipped It is
PRE-ALPHA quality software. The code&#8202;&mdash;&#8202;written in Python by a
programmer who has only recently started learning that
language&#8202;&mdash;&#8202;is of SUSPECT quality, and there are NO unit tests
and NO Q.A. professionals (or, indeed, testers of any kind) have vetted it.

There is at least a 70% chance that There, I Clipped It will FORMAT your hard
drive and email ABUSE to your boss and/or parole officer.

Oh, and it only works for text.

## I Don't Care. I Want It. How Do I Get It?

First, you need to make sure you own/fulfil the following requirements:

1. An iOS device with the following apps installed:

   - Pythonista
   - Workflow
   - Pushover

2. At least one OS X computer with Python 3 and pip installed. (Windows version
   coming soon!)

3. A Dropbox account.

## OS X Installation

1. Obtain the scripts, placing them in your Dropbox:

       cd ~/Dropbox
       git clone https://github.com/sedm0784/thereiclippedit.git

2. (Optional, recommended) Create a new virtualenv and activate it.

3. Run the installation script:

       cd thereiclippedit
       ./install_thereiclippedit.py -u YOUR_PUSHOVER_USER_KEY -c THE_COMPUTER_NAME

### That Sounds a Bit Dodge. What Does the Installation Script Do?

1. Installs the Python requirements: requests and gntp,

2. Configures and installs the launchd plist to the location:
   `~/Library/LaunchAgents/`

3. Configures and installs the There, I Clipped It Automator workflow as a
   Service.

4. GENTLY reminds you (where) to set up a keyboard shortcut in System
   Preferences in order to invoke There, I Clipped It quickly.

## iOS Installation

1. Install the [There, I Clipped It workflow](https://workflow.is/workflows/a4b469cd702541fab1e3958b26d156ab),

2. Edit the workflow with the names of the computers that you used during OS X
   Installation,

3. (Optional, recommended) Set up some method of firing off the Workflow
   quickly. I added a shortcut to the [Launch Center app](), but you could
   create a home screen shortcut or Today view widget if you prefer.

[1]: Read: because I am a cheapskate.
