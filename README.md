## Visual workspace switcher
![ws2](https://github.com/CarloCattano/workspacer/assets/17380530/5d28bcfc-3270-46b2-8372-33d504880855)
![image](https://github.com/CarloCattano/workspacer/assets/17380530/3641ef97-ab04-48a4-aa3e-922ee42b1fbc)


made for [Hyprland](https://hyprland.org)

bind the _workspaced.py_ to a key or to your bar, and get a convenient way to switch between workspaces with previews of the windows in each workspace.

#### configuration

you need to run the _workspace_listener.sh_ script in the background to get the previews of the windows in each workspace.

In my case I write it into ~/.config/hypr/hyrland.conf

```bash
exec-once = $HOME/scripts/hypr/workspace_listener.sh
```

It will snapshot the workspaces, whenever:
- a workspace is created/changed/destroyed
- an application window is closed

by using Hyprland own's [IPC](https://wiki.hyprland.org/IPC/) socket

#### requeriments:

- ```grim```  cli screenshot tool
- ```jq``` json parser

#### example keybinding

```bash
bind = $Mod , Y, exec , $HOME/scripts/hypr/workspaced.py
```

#### floating rule
```bash
windowrule = float, title:^(Workspace Selector)$
```

#### waybar example 
trigger when clicking on bar title
```
"hyprland/window": {
		"format": "{}",
		"separate-outputs": true,
	            "on-click":"/home/YOUR_USER/../../workspaced.py",
},
```

### TODO : 
    - add a way to navigate the options with vim keys hjkl
    - find faster screenshot mechanism
	- test with animations
    - prevent double execution of the script or instances of the script
~~When a window is removed , check if the workspace is empty and remove it~~
