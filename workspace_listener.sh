#!/bin/sh

screen_shot() {     # take a screenshot of the current workspace
    sleep 2
    grim /tmp/workspace"$(hyprctl activeworkspace | head -n1 | cut -d " " -f 3)".png
}

rm_ws() {        # remove the destroyed workspace screenshot
    rm /tmp/workspace"$1".png -f
}

handle() {
  case $1 in
      workspace*) screen_shot ;;
      destroyworkspace*) rm_ws "$(echo $1 | cut -d '>' -f 3)" ;;
  esac
}

socat -U - UNIX-CONNECT:/tmp/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock | while read -r line; do handle "$line"; done

