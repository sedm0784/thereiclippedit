# There, I Clipped It

## What *Is* This?

There, I Clipped It is a lightweight, cross-platform, and thoroughly UNHOLY
amalgam of scripts, tools, and configuration settings that make it EASY to
INSTANTLY squirt your clipboard from your iOS devices to your computers and
vice versa.

I made it because it was fun to do, and in order to avoid having to be LOCKED
IN to any of the numerous commercial solutions for this problem<sup>1</sup>.

It is named in homage to the [meme wherein repairs are made in an inelegant but
effective style](http://google.com/search?q=there+i+fixed+it). If There, I
Clipped It existed outside of your computing device, it would consist entirely
of gaffer tape and odd bits of cardboard.

<sup>1: Read: because I am a cheapskate.</sup>

## How Does It Work?

### Squirting the iOS Clipboard to a Computer

You invoke the There, I Clipped It workflow in the [Workflow
app](http://workflow.is/). It asks you which of your computers you want your
clipboard to be SQUIRTED to. It then saves the contents of your clipboard to a
file in your Dropbox. The corresponding computer, which is watching like a HAWK
for that file to be created (via
[launchd](https://en.wikipedia.org/wiki/Launchd)), then runs a Python script to
replace your clipboard with the file's contents. A Growl notification pops up
to inform you your clipboard is ready to SATE your PASTE-FURY.

*(Windows does not include a method of creating watch folders as part of the
operating system. It's possible to create a program that carries out this task,
but one of the reasons I decided to write There, I Clipped It, was because I
didn't want to have a dedicated program running 24/7 just to provide this
functionality. As such, in order to copy the newly received clipboard contents,
you must manually initiate the copy with a keyboard shortcut: Ctrl+Alt+C)*

### Squirting Your Computer's Clipboard to iOS

You press a keyboard shortcut<sup>2</sup>. This invokes the There, I Clipped It
Service, which runs a Python script that reads your clipboard and sends it to
your iOS device as a push notification (via the [Pushover
app](http://pushover.net/)). When your iOS device pings, you open the
notification and tap on a link, which runs a script in the [Pythonista
app](http://omz-software.com/pythonista/) that STUFFS the copied text into your
your iOS clipboard.

<sup>2: I'm using Command+Option+Ctrl+V on OS X and Ctrl+Alt+V on Windows.</sup>

## Sounds Good; I Want It.

You really don't.

Whilst I use it on several computers, and it works, There, I Clipped It is
PRE-ALPHA quality software. The code&#8202;&mdash;&#8202;written in Python by a
programmer who has only recently started learning that
language&#8202;&mdash;&#8202;is of SUSPECT quality, there are NO unit tests,
and NO Q.A. professionals (or, indeed, testers of any kind) have vetted it.

There is at least a 70% chance that There, I Clipped It will FORMAT your hard
drive and email ABUSE to your boss and/or parole officer.

Oh, and it only works for text.

## I Don't Care. I Want It. How Do I Get It?

Okay, fine. First, you need to make sure you own/fulfil the following
requirements:

1. An iOS device with the following apps installed:

   - [Workflow](http://workflow.is/)
   - [Pushover](http://pushover.net/)
   - [Pythonista](http://omz-software.com/pythonista/)

2. At least one computer with Python 3 and pip installed.

3. (Optional) [Growl](http://growl.info/)

4. A Dropbox account.

## Installation on a Computer

1. Obtain the scripts, placing them in your Dropbox:

    ```sh
    cd ~/Dropbox
    git clone https://github.com/sedm0784/thereiclippedit.git
    ```

2. (Optional, recommended) Create a new virtualenv and activate it.

3. Run the installation script:

    ```sh
    cd thereiclippedit
    ./install_thereiclippedit.py -u YOUR_PUSHOVER_USER_KEY -c THE_COMPUTER_NAME
    ```

### That Sounds a Bit Dodge. What Does the Installation Script Do?

1. Installs the Python requirements: requests, pyperclip, and gntp,

2. *OS X:* Configures and installs the launchd plist to the location:
   `~/Library/LaunchAgents/`

3. *OS X:* Configures and installs the There, I Clipped It Automator workflow as a
   Service. (in `~/Library/Services/`

4. *OS X:* GENTLY reminds you (where) to set up a keyboard shortcut in System
   Preferences in order to invoke There, I Clipped It quickly.

5. *Windows:* Configures and installs shortcuts for pushing and pulling you
   clipboard to your "Programs" folder. The push shortcut has the keyboard
   shortcut Ctrl+Alt+V and the pull shortcut has the keyboard shortcut
   Ctrl+Alt+C. If you want to use different shortcuts, you can edit them by
   right-clicking on the installed shortcut files and selecting "Properties".

## iOS Installation

1. Install the [There, I Clipped It workflow](https://workflow.is/workflows/a4b469cd702541fab1e3958b26d156ab),

2. Edit the workflow with the names of the computers that you used during OS X
   Installation,

3. (Optional, recommended) Set up some method of firing off the Workflow
   quickly. I added a shortcut to the [Launch Center Pro
   app](http://contrast.co/launch-center-pro/), but you could create a home
   screen shortcut or Today view widget if you prefer.

4. Get the
   [grab_clipboard.py](https://raw.githubusercontent.com/sedm0784/thereiclippedit/master/grab_clipboard.py)
   script into Pythonista. The obvious way would be to whizz it on over into
   your iOS clipboard with There, I Clipped It, but there's a bit of a
   chicken-and-egg situation going on there. Sorry, you're on your own for this
   one. Worst-case scenario you're just going to have to type it in.

5. Bonus feature! In order to squirt directly from iOS apps, install the
   [There, I Clipped It Action
   Extension](https://workflow.is/workflows/e6b0999ec8de4c76939e13c49432bcc2)
   too.

## Roadmap

As far as I'm concerned, There, I Clipped It is COMPLETE, because it Works for
Me&trade;. However, there *are* some things that could be added:

- The requirements list is both SPECIFIC and ONEROUS. I selected the various
  tools simply because those were the ones I already had installed, but There,
  I Clipped It is conceptually pretty simple, and each of the tools used has
  any number of possible replacements. It might be nice to implement some
  alternatives (e.g. Launch Center Pro instead of Workflow, Prowl instead of
  Pushover) and allow the use of these.

- Distribution: the contents of the repository could be made available as a zip
  file.

- Configurable `sharedboards` location: the advantage of storing *everything*
  in Dropbox is that you only have to download/clone it once. However, you
  might reasonably be reluctant to clutter up your Dropbox with the entire
  tool. It should be possible to only have the `sharedboards` folder within
  Dropbox.

- Might be nice to offer notifications using OS X's Notification Center instead
  of Growl.

- You currently have to inform There, I Clipped It of your Pushover User Key
  during installation. Pushover offers a feature which automates this, so users
  don't even have to *see* the UNGAINLY key. My predicted audience of There, I
  Clipped It is zero, but if it turns out more people use it than expected, I
  might look into this one.

- When sending text from an iOS device, you can pick a destination, but when
  sending text from a computer, it is broadcast to *all* your iOS devices. This
  is how I like it, but Pushover allows you to specify a destination: maybe you
  would like There, I Clipped It to, also.

- I should probably better document the contents of the repository. What
  everything does and how it all works.
