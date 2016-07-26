set WshShell = WScript.CreateObject("WScript.Shell")
programs_path = WshShell.SpecialFolders("Programs")
set oShellLink = WshShell.CreateShortcut(programs_path & "\There, I Clipped It.lnk")
oShellLink.TargetPath = "%%PUSH_SCRIPT_PATH%%"
oShellLink.WindowStyle = 7
oShellLink.Hotkey = "ALT+CTRL+v"
oShellLink.Description = "There, I Clipped It"
oShellLink.WorkingDirectory = programs_path
oShellLink.Arguments = "%%USER_KEY%%"
oShellLink.Save
