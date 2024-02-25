#!/sbin/python3
import gi
import os
import glob

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

class WorkspaceSelector(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Workspace Selector")
        self.set_default_size(800, 600)
        
        marg = 42

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=marg)
        self.add(box)

            
        box.set_margin_top(marg)
        box.set_margin_bottom(marg)
        box.set_margin_start(marg)
        box.set_margin_end(marg)

        grid = Gtk.Grid()
        
        grid.set_column_spacing(marg)  # Add padding between columns
        grid.set_row_spacing(marg)     # Add padding between rows
        
        box.pack_start(grid, True, True, 0)  # Add the grid to the box
        
        self.grid = grid

        workspace_files = sorted(glob.glob('/tmp/workspace*.png'))
        num_workspaces = len(workspace_files)

        if num_workspaces > 2:
            self.num_columns = 3
            self.num_rows = (num_workspaces + self.num_columns - 1) // self.num_columns
        else:
            self.num_columns = num_workspaces
            self.num_rows = 1

        self.num_rows = (num_workspaces + self.num_columns - 1) // self.num_columns
        self.load_workspace_images(workspace_files)
       
    def load_workspace_images(self, workspace_files):
        # Remove existing widgets from the grid
        for child in self.grid.get_children():
            self.grid.remove(child)

        # Calculate number of rows and columns for the grid
        window_width = self.get_size()[0]
        image_width = window_width // self.num_columns
        image_height = image_width * 2 // 2  # aspect ratio 

        for i, workspace_file in enumerate(workspace_files):
            image = Gtk.Image()
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(workspace_file, image_width, image_height)
            image.set_from_pixbuf(pixbuf)
            button = Gtk.Button()
            button.add(image)
            button.connect("clicked", self.on_workspace_selected, i)
            column = i % self.num_columns
            row = i // self.num_columns
            self.grid.attach(button, column, row, 1, 1)

    def on_workspace_selected(self, button, workspace_index):
        os.system(f'hyprctl dispatch workspace {workspace_index + 1}')
        self.destroy()

win = WorkspaceSelector()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

