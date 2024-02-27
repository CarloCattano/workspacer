#!/bin/sh

rm /tmp/workspace*.png -f

screen_shot() {
    # Store the x, y, width, and height values of the active monitor into variables
    read x y width height <<< $(hyprctl monitors -j | jq -r '.[] | select(.focused) | "\(.x) \(.y) \(.width) \(.height)"')

    offset_x=$x
    offset_y=$y

    geometry="${offset_x},${offset_y} ${width}x${height}"

    active_workspace=$(hyprctl activeworkspace -j | jq '.id')
    grim -t png -l1 -g "$geometry" "/tmp/workspace$active_workspace.png"
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
