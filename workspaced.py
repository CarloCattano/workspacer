#!/usr/bin/env python3
import gi
import os
import glob

gi.require_version('Gtk', '3.0')

# Import Gdk module
from gi.repository import Gtk, GdkPixbuf, Gdk, GLib

class WorkspaceSelector(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Workspace Selector")       

        width = 900
        height = 700

        marg = 42
        self.set_default_size(width, height)        #e(800, 700)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=marg)
        self.add(box)
        box.set_margin_top(marg)
        box.set_margin_bottom(marg)
        box.set_margin_start(marg)
        box.set_margin_end(marg)

        grid = Gtk.Grid()

        grid.set_column_spacing(marg)
        grid.set_row_spacing(marg)

        box.pack_start(grid, True, True, 0)  # Add the grid to the box

        self.grid = grid

        workspace_files = sorted(glob.glob('/tmp/workspace*.png'))
        num_workspaces = len(workspace_files)

        if num_workspaces > 3:
            self.num_columns = 3
            self.num_rows = (num_workspaces + self.num_columns - 1) // self.num_columns
        elif num_workspaces <= 3:
            self.num_rows = 1
            self.num_columns = num_workspaces
            box.set_margin_top(height / 2)
            box.set_margin_bottom(height / 2)
        if num_workspaces == 1:
            self.num_rows = 1
            self.num_columns = 1
            box.set_margin_top(height / 2)
            box.set_margin_bottom(height / 2)

        self.load_workspace_images(workspace_files)

    def load_workspace_images(self, workspace_files):
        # Remove existing widgets from the grid
        for child in self.grid.get_children():
            self.grid.remove(child)

        # Get the current workspace
        current_workspace = int(os.popen("hyprctl activeworkspace -j | jq '.id'").read())

        # Calculate number of rows and columns for the grid
        window_width = self.get_size()[0]
        image_width = window_width // self.num_columns
        image_height = image_width 

        for i, workspace_file in enumerate(workspace_files):
            image = Gtk.Image()
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(workspace_file, image_width, image_height)
            image.set_from_pixbuf(pixbuf)
            button = Gtk.Button()
            button.add(image)
            button.connect("clicked", self.on_workspace_selected, i)
            column = i % self.num_columns
            row = i // self.num_columns

            # current workspace button style
            if i + 1 == current_workspace:
                button.get_style_context().add_class("current-workspace")
            else: 
                button.get_style_context().add_class("workspace-button")
            
            self.grid.attach(button, column, row, 1, 1)

        self.connect("key-press-event", self.on_key_press)

    def on_workspace_selected(self, button, workspace_index):
        
        current = int(os.popen("hyprctl activeworkspace -j | jq '.id'").read())
        
        if current == workspace_index + 1:
            self.destroy()
        
        elif current != workspace_index + 1:
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
# Apply CSS style for highlighting current workspace button
css_provider = Gtk.CssProvider()
css_provider.load_from_data("""
    .current-workspace {
        background-color: yellow;
    }

    .workspace-button {
        background-color: transparent;
    }

    .workspace-button:focus {
        background-color: transparent;
    }
""")
screen = Gdk.Screen.get_default()
style_context = win.get_style_context()
style_context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

Gtk.main()

