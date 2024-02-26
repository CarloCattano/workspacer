#!/bin/sh

rm /tmp/workspace*.png -f

# TODO : find a way to make screenshots in periods of time if we have 
# already taken a screenshot of the current workspace
# manage case where ws 1 is deleted and the workspaces are shifted
# depending on user configuration
# TODO
# compare the current time with the time of the last screenshot in the workspace corresponding to the current workspace0

screen_shot() {     # take a screenshot of the current workspace
    active_workspace=$(hyprctl activeworkspace -j | jq '.name')
    # hyprctl keyword animations:enabled false 2> /dev/null
    sleep 0.6
    grim -l1 /tmp/workspace"$active_workspace".png
    # hyprctl keyword animations:enabled true 2> /dev/null
}

rm_ws() {        # remove the destroyed workspace screenshot
    rm /tmp/workspace"$1".png -f
}

handle() {
  case $1 in
      workspace*) screen_shot ;;
      createworkspace*) screen_shot ;;
      destroyworkspace*) rm_ws "$(echo $1 | cut -d '>' -f 3)" ;;
  esac
}

socat -U - UNIX-CONNECT:/tmp/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock | while read -r line; do handle "$line"; done

