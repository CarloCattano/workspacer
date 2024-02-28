#!/usr/bin/env python3
import gi
import os
import glob
import json

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, GdkPixbuf, Gdk

current_workspace = None


class WorkspaceSelector(Gtk.Window):
    def __init__(self):
        # Take a screenshot of the current workspace before launching the window
        current_workspace = int(
            os.popen("hyprctl activeworkspace -j | jq '.id'").read()
        )
        geometry = (
            os.popen(
                "hyprctl monitors -j | jq -r '.[] | select(.focused) | \"\(.x) \(.y) \(.width) \(.height)\"'"
            )
            .read()
            .split()
        )
        offset_x = int(geometry[0])
        offset_y = int(geometry[1])
        width = int(geometry[2])
        height = int(geometry[3])
        geometry = f"{offset_x},{offset_y} {width}x{height}"
        # os.system(f'grim -l1 -g {geometry} /tmp/workspace{current_workspace}.png')
        os.system(f"grim -type jpeg -q 50 /tmp/workspace{current_workspace}.png")
        # GTK START
        Gtk.Window.__init__(self, title="Workspace Selector")
        width = 1000
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
        self.grid = grid

        box.pack_start(grid, True, True, 0)
        self.set_app_paintable(True)

        # self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 0))  # Set transparent background
        workspace_files = sorted(glob.glob("/tmp/workspace*.png"))
        num_workspaces = len(workspace_files)

        if num_workspaces > 10:
            self.num_columns = 5
        if num_workspaces < 10 and num_workspaces > 3:
            self.num_columns = 3
        elif num_workspaces <= 3:
            grid.set_row_homogeneous(True)
            self.num_rows = 1
            self.num_columns = num_workspaces
            self.set_default_size(width, height // 2 * self.num_rows)

            if num_workspaces == 1:
                self.num_rows = 1
                self.num_columns = 1

        # TODO : abstract all this file thins
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        color_conf_path = os.path.join(script_dir, "colors.conf")
        if not os.path.isfile(color_conf_path):
            print(
                "Error: colors.conf not found on script folder ",
                color_conf_path,
            )
            exit()

        # Load colors from config file
        with open(color_conf_path, "r") as color_file:
            colors = json.load(color_file)

        self.current_workspace_color = colors.get("current_workspace")
        self.workspace_button_color = colors.get("workspace_button")
        self.workspace_button_focus_color = colors.get("workspace_button_focus")
        # ---------------------------------------------------------------------

        self.load_workspace_images(workspace_files)

    def load_workspace_images(self, workspace_files):
        global current_workspace

        if current_workspace is None:
            current_workspace = int(
                os.popen("hyprctl activeworkspace -j | jq '.id'").read()
            )

        # Calculate number of rows and columns for the grid
        window_width = self.get_size()[0]
        image_width = window_width // self.num_columns
        image_height = image_width

        # Load the workspace images
        for i, workspace_file in enumerate(workspace_files):
            image = Gtk.Image()
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                workspace_file, image_width, image_height
            )
            image.set_from_pixbuf(pixbuf)
            button = Gtk.Button()
            button.add(image)

            # make buttons less high
            button.set_size_request(image_width, image_height / 2)
            button.set_relief(Gtk.ReliefStyle.NONE)

            img_index = int(workspace_file.split("workspace")[1].split(".png")[0]) - 1

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
            os.system(f"hyprctl dispatch workspace {workspace_index + 1}")
            self.destroy()

    def on_key_press(self, widget, event):
        keyval = event.keyval
        if keyval == Gdk.KEY_Escape or chr(keyval) == "q":
            self.destroy()


win = WorkspaceSelector()
win.connect("destroy", Gtk.main_quit)
win.show_all()
win.set_focus(None)
css_provider = Gtk.CssProvider()
css_provider.load_from_data(
    f"""

    .current-workspace {{
        background-color: {win.current_workspace_color};
    }}

    .workspace-button {{
        background-color: {win.workspace_button_color};

    }}
    .workspace-button:focus {{
        background-color: {win.workspace_button_focus_color};
    }}
"""
)
screen = Gdk.Screen.get_default()
style_context = win.get_style_context()
style_context.add_provider_for_screen(
    screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
Gtk.main()
