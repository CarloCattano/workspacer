#!/usr/bin/env python3
import gi
import os
import glob

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GdkPixbuf, Gdk, GLib

current_workspace = int(os.popen("hyprctl activeworkspace -j | jq '.id'").read())

# get the geometry of the active monitor
geometry = os.popen("hyprctl monitors -j | jq -r '.[] | select(.focused) | \"\(.x) \(.y) \(.width) \(.height)\"'").read().split()
offset_x = int(geometry[0])
offset_y = int(geometry[1])
width = int(geometry[2])
height = int(geometry[3])

geometry = f"{offset_x},{offset_y} {width}x{height}"

os.system(f'grim -l1 -g {geometry} /tmp/workspace{current_workspace}.png')

class WorkspaceSelector(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Workspace Selector")

        width = 800
        height = 700

        marg = 42
        self.set_default_size(width, height)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=marg)
        self.add(box)
        box.set_margin_top(marg * 3)
        box.set_margin_bottom(marg * 3)
        box.set_margin_start(marg)
        box.set_margin_end(marg)

        grid = Gtk.Grid()

        grid.set_column_homogeneous(True)
       
        grid.set_column_spacing(marg)
        grid.set_row_spacing(marg)

        box.pack_start(grid, True, True, 0)

        self.grid = grid

        # make background transparent
        self.set_app_paintable(True)
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 0))  # Set transparent background

        workspace_files = sorted(glob.glob('/tmp/workspace*.png'))
        num_workspaces = len(workspace_files)

        if num_workspaces > 3:
            # grid.set_row_homogeneous(True)
            self.num_columns = (num_workspaces + 2) // 2
            self.num_rows = (num_workspaces + self.num_columns - 2) // self.num_columns
        elif num_workspaces <= 3:
            grid.set_row_homogeneous(True)
            self.num_rows = 1
            self.num_columns = num_workspaces
            self.set_default_size(width, height // 2 * self.num_rows)

            if num_workspaces == 1:
                self.num_rows = 1
                self.num_columns = 1

        self.load_workspace_images(workspace_files)

    def load_workspace_images(self, workspace_files):
        global current_workspace  
        
        if current_workspace is None:
            current_workspace = int(os.popen("hyprctl activeworkspace -j | jq '.id'").read())

        # Calculate number of rows and columns for the grid
        window_width = self.get_size()[0]
        image_width = window_width // self.num_columns
        image_height = image_width 
        
        
        # Load the workspace images
        for i, workspace_file in enumerate(workspace_files):
            image = Gtk.Image()
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(workspace_file, image_width, image_height)
            image.set_from_pixbuf(pixbuf)
            button = Gtk.Button()
            button.add(image)

            # make buttons less high
            button.set_size_request(image_width, image_height / 2)
            button.set_relief(Gtk.ReliefStyle.NONE)

            img_index = int(workspace_file.split('workspace')[1].split('.png')[0]) - 1

            button.connect("clicked", self.on_workspace_selected, img_index)

            column = i % self.num_columns
            row = i // self.num_columns
            
            # current workspace marker
            if img_index + 1 == current_workspace:
                button.get_style_context().add_class("current-workspace")
            else: 
                button.get_style_context().add_class("workspace-button")
                
            self.grid.attach(button, column, row, 1, 1)

        self.connect("key-press-event", self.on_key_press)

    def on_workspace_selected(self, button, workspace_index):
        global current_workspace  # Use the global variable
        
        if current_workspace == workspace_index + 1:
            self.destroy()
        else:
            os.system(f'hyprctl dispatch workspace {workspace_index + 1}')
            self.destroy()

    def on_key_press(self, widget, event):
        keyval = event.keyval
        if keyval == Gdk.KEY_Escape or chr(keyval) == 'q':
            self.destroy()
      
win = WorkspaceSelector()
win.connect("destroy", Gtk.main_quit)
win.show_all()
win.set_focus(None)
css_provider = Gtk.CssProvider()
css_provider.load_from_data("""

    .current-workspace {
        background-color: rgba(255, 255, 0, 0.5);
    }
                       
    .workspace-button {
        background-color: rgba(0, 0, 0, 0);

    }
    .workspace-button:focus {
        background-color: rgba(0, 0, 0, 0);
    }
""")
screen = Gdk.Screen.get_default()
style_context = win.get_style_context()
style_context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
Gtk.main()

