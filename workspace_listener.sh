#!/bin/sh

rm /tmp/workspace*.png -f

# TODO : find a way to make screenshots in periods of time if we have 
# already taken a screenshot of the current workspace
# manage case where ws 1 is deleted and the workspaces are shifted
# depending on user configuration
# TODO
# compare the current time with the time of the last screenshot in the workspace corresponding to the current workspace0

screen_shot() {     # take a screenshot of the current workspace
    sleep 0.5
    active_workspace=$(hyprctl activeworkspace -j | jq '.id')
    grim -l1 /tmp/workspace$active_workspace.png
}

rm_ws() {        # remove the destroyed workspace screenshot
    rm /tmp/workspace$1.png -f
}

handle() {
  case $1 in
      workspace*) screen_shot ;;
      createworkspace*) screen_shot ;;
      destroyworkspace*) rm_ws "$(echo $1 | cut -d '>' -f 3)" ;;
      closewindow*) screen_shot ;;
  esac
}

socat -U - UNIX-CONNECT:/tmp/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock | while read -r line; do handle "$line"; done

