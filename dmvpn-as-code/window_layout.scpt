# AppleScript for Demo Window layout
# execute with `osascript window_layout.scpt`

tell application "iTerm"
	activate
	tell current window
		create tab with default profile
	end tell
	set pane_1 to (current session of current window)

	tell pane_1
		set pane_3 to (split horizontally with same profile)
	end tell

	tell pane_1
		set pane_2 to (split vertically with same profile)
	end tell

	tell pane_3
		set pane_4 to (split vertically with same profile)
	end tell


	tell pane_1
		write text "workon cicd-dmvpn"
	end tell

	tell pane_2
		write text "workon cicd-dmvpn"
		write text "cd virl/test"
		write text "virl nodes"
	end tell

	tell pane_3
		write text "workon cicd-dmvpn"
		write text "cd logs/"
		write text "tail -f ncs-python-vm.log"
	end tell

	tell pane_4
		write text "workon cicd-dmvpn"
		write text "cd packages/dmvpn/"
		write text "ncs_hot_reload"

	end tell



end tell
