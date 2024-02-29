#!/bin/sh

rm /tmp/workspace*.jpg -f

screen_shot() 
{
    # Store the x, y, width, and height values of the active monitor into variables
    read x y width height <<< $(hyprctl monitors -j | jq -r '.[] | select(.focused) | "\(.x) \(.y) \(.width) \(.height)"')

    geometry="${x},${y} ${width}x${height}"

    active_workspace=$(hyprctl activeworkspace -j | jq '.id')
    grim -t jpeg -q 50 -g "$geometry" "/tmp/workspace$active_workspace.jpg"
}

closed_window() 
{    
    #when a window is closed, check if it was the last window in the workspace
    is_last_window=$(hyprctl activeworkspace -j | jq '.windows')
 
    if [ $is_last_window -eq 0 ]; then
        rm /tmp/workspace$1.jpg -f
    else
        screen_shot
    fi
}

rm_ws() {                       # remove the destroyed workspace screenshot
    rm /tmp/workspace$1.jpg -f
}

handle() 
{
  case $1 in
      workspace*) screen_shot ;;
      createworkspace*) screen_shot ;;
      destroyworkspace*) rm_ws "$(echo $1 | cut -d '>' -f 3)" ;;
      closewindow*) closed_window;;
  esac
}

socat -U - UNIX-CONNECT:/tmp/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock | while read -r line; do handle "$line"; done

# https://wiki.hyprland.org/IPC/

