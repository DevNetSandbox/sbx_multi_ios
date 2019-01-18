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

	tell pane_1
		write text "workon cicd-evpn; cat Makefile"
	end tell

	tell pane_2
		write text "workon cicd-evpn"
		write text "open http://opk-git.cisco.com/netdevops/cicd-evpn/pipelines"
		write text "cd virl/prod"
		write text "virl nodes"
		
	end tell

	tell pane_3
		write text "workon cicd-evpn; atom ."
	end tell

end tell
