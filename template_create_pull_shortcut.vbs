set WshShell = WScript.CreateObject("WScript.Shell")
programs_path = WshShell.SpecialFolders("Programs")
set oShellLink = WshShell.CreateShortcut(programs_path & "\There, I Clipped It Pull.lnk")
oShellLink.TargetPath = "%%PULL_SCRIPT_PATH%%"
oShellLink.WindowStyle = 7
oShellLink.Hotkey = "ALT+CTRL+c"
oShellLink.Description = "There, I Clipped It"
oShellLink.WorkingDirectory = programs_path
oShellLink.Arguments = "%%CLIPBOARD_PATH%%"
oShellLink.Save
