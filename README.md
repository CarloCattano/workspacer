## Visual Workspace Switcher

![Workspace Switcher](https://github.com/CarloCattano/workspacer/assets/17380530/5d28bcfc-3270-46b2-8372-33d504880855)

![Image](https://github.com/CarloCattano/workspacer/assets/17380530/3641ef97-ab04-48a4-aa3e-922ee42b1fbc)

Developed for [Hyprland](https://hyprland.org)

**Workspacer** is a utility designed to enhance workspace management by providing a visual overview of each workspace's contents, facilitating seamless switching between them.

### Requirements

Ensure you have the following dependencies installed:

- `grim`: CLI screenshot tool
- `jq`: JSON parser
- `socat`: Multipurpose relay


### Usage

Simply bind the `workspaced.py` script to a key or integrate it into your system bar for quick access to workspace previews and switching.

#### Example Keybinding

```bash
bind = $Mod , Y, exec , $HOME/scripts/hypr/workspaced.py
```

#### Configuration

To enable previews of windows within each workspace, run the `workspace_listener.sh` script in the background. Configure it in your system settings or a configuration file like `~/.config/hypr/hyrland.conf`.

```bash
exec-once = $HOME/scripts/hypr/workspace_listener.sh
```

This script utilizes Hyprland's own [IPC](https://wiki.hyprland.org/IPC/) socket to snapshot the workspaces whenever a workspace is created/changed/destroyed or an application window is closed. 

##### Colors

You can modify the colors used by the Workspace Switcher by editing the colors.conf file in the script's directory. For example:

```json
{
  "current_workspace": "rgba(0, 255, 0, 0.6)",
  "workspace_button": "rgba(0, 0, 0, 0)",
  "workspace_button_focus": "rgba(0, 0, 0, 0)"
}
```


#### Floating Rule

```bash
windowrule = float, title:^(Workspace Selector)$
```

#### Waybar Integration

Example configuration for Waybar, trigger the Workspace Switcher when clicking on the bar title:

```json
"hyprland/window": {
    "format": "{}",
    "separate-outputs": true,
    "on-click":"/home/YOUR_USER/../../workspaced.py",
}
```

### TODO

- Implement navigation with vim keys (hjkl)
- Optimize screenshot mechanism for faster performance
- Test compatibility with animations
- Prevent script from executing multiple instances
- ~~Automatically remove empty workspaces when windows are closed~~