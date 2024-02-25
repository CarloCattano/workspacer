#!/bin/sh

# delete previous screenshots if any
rm /tmp/workspace*.png -f

# TODO : find a way to make screenshots in periods of time if we have 
# already taken a screenshot of the current workspace

screen_shot() {     # take a screenshot of the current workspace
    # hyprctl keyword animations:enabled false 2> /dev/null
    sleep 1.42
    grim -l1 /tmp/workspace"$(hyprctl activeworkspace | head -n1 | cut -d " " -f 3)".png
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

