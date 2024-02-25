#!/bin/sh

# delete previous screenshots if any
rm /tmp/workspace*.png -f

# TODO : find a way to make screenshots in periods of time if we have 
# already taken a screenshot of the current workspace
# manage case where ws 1 is deleted and the workspaces are shifted
# depending on user configuration

# append current time to the screenshot name
# compare the current time with the time of the last screenshot in the workspace corresponding to the current workspace0
# if the difference is greater than 25 seconds, take a new screenshot

shot_intervals() {
    active_workspace=$(hyprctl activeworkspace -j | jq '.name')
    if [ ! -f /tmp/workspace"$active_workspace".png ]; then
        screen_shot
        return
    fi

    last_screenshot_time=$(stat -c %Y /tmp/workspace"$active_workspace".png)
    current_time=$(date +%s)
    difference=$(($current_time - $last_screenshot_time))
    
    echo "difference: $difference"

    if [ $difference -gt 8 ]; then
        screen_shot
    fi
}

screen_shot() {     # take a screenshot of the current workspace
    # hyprctl keyword animations:enabled false 2> /dev/null
    sleep 0.6
    grim -l1 /tmp/workspace"$(hyprctl activeworkspace -j | jq '.name')".png
    # hyprctl keyword animations:enabled true 2> /dev/null
}

rm_ws() {        # remove the destroyed workspace screenshot
    rm /tmp/workspace"$1".png -f
}

handle() {
  case $1 in
      workspace*) shot_intervals ;; #screen_shot ;;
      createworkspace*) shot_intervals ;;
      destroyworkspace*) rm_ws "$(echo $1 | cut -d '>' -f 3)" ;;
  esac
}

socat -U - UNIX-CONNECT:/tmp/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock | while read -r line; do handle "$line"; done

