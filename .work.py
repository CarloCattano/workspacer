#!/usr/bin/env python3
import gi
import os
import glob

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

class WorkspaceSelector(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Workspace Selector")
        self.set_default_size(800, 600)

        grid = Gtk.Grid()
        grid.set_column_spacing(20)  # Add padding between columns
        grid.set_row_spacing(20)     # Add padding between rows

        self.add(grid)
        self.grid = grid

        # List all workspace screenshot files
        workspace_files = sorted(glob.glob('/tmp/workspace*.png'))
        num_workspaces = len(workspace_files)

        # Initialize size parameters
        self.num_columns = 3  # You can adjust this as needed
        self.num_rows = (num_workspaces + self.num_columns - 1) // self.num_columns

        self.load_workspace_images(workspace_files)

        self.connect("size-allocate", self.on_window_resized)

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

    def on_window_resized(self, widget, allocation):
        # Recalculate number of columns based on window width
        window_width = allocation.width
        self.num_columns = max(1, window_width // 200)  # Adjust 200 according to your needs
        self.num_rows = (num_workspaces + self.num_columns - 1) // self.num_columns

        # Reload workspace images based on updated grid configuration
        workspace_files = sorted(glob.glob('/tmp/workspace*.png'))
        self.load_workspace_images(workspace_files)

    def on_workspace_selected(self, button, workspace_index):
        os.system(f'hyprctl dispatch workspace {workspace_index + 1}')
        self.destroy()

win = WorkspaceSelector()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

