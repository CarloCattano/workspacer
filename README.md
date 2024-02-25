## Visual workspace switcher
![ws2](https://github.com/CarloCattano/workspacer/assets/17380530/5d28bcfc-3270-46b2-8372-33d504880855)


made for [Hyprland](https://hyprland.org)

bind the _workspaced.py_ to a key or to waybar , and get a convenient way to switch between workspaces
with previews of the windows in each workspace.

#### configuration

you need to run the _workspace_listener.sh_ script in the background to get the previews of the windows in each workspace.
In my case I write it into ~/.config/hypr/hyrland.conf

```bash
exec-once = $HOME/scripts/hypr/workspace_listener.sh
```
It will continue to snapshot the workspaces, whenever there is a change in workspace, by using Hyprland own's IPC.

requeriments:
    - grim - cli screenshot tool
    - jq - json parser

    - ~todo~

#### example keybinding

```bash
    bind = $Mod , Y, exec , $HOME/scripts/hypr/workspaced.py
```

#### floating rule
```bash
    windowrule = float, title:^(Workspace Selector)$
```

- TODO: 
    find a fast and low res snapshot method
    when switching too fast, 2 seconds delay is too little to get the screenshot in time
    and also respect any possible animation duration
    - add a way to navigate the options with vim keys hjkl
