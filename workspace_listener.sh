#!/bin/sh

rm /tmp/workspace*.png -f

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

# https://wiki.hyprland.org/IPC/
