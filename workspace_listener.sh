#!/bin/sh

screen_shot() {
    grim /tmp/workspace"$(hyprctl activeworkspace | head -n1 | cut -d " " -f 3)".png
}

rm_ws() {
    rm /tmp/workspace"$1".png -f
}

handle() {
  case $1 in
      workspace*) screen_shot ;;
      # take the data from the socket and pass it to the function
      destroyworkspace*) rm_ws "$(echo $1 | cut -d '>' -f 3)" ;;
  esac
}

socat -U - UNIX-CONNECT:/tmp/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock | while read -r line; do handle "$line"; done

