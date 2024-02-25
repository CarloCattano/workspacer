## Visual workspace switcher

bind the _workspaced.py_ to a key or to waybar , and get a convenient way to switch between workspaces
with previews of the windows in each workspace.

#### configuration

you need to run the _workspace_listener.sh_ script in the background to get the previews of the windows in each workspace.
In my case I write it into hypr/hyrland.conf

```bash
exec-once = $HOME/scripts/hypr/workspace_listener.sh
```
It will continue to snapshot the workspaces, whenever there is a change in workspace

- TODO: 
    find a fast and low res snapshot method


