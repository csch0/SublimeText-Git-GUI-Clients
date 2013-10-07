import sublime
import sublime_plugin

import os
import subprocess


class GgcOpenCommand(sublime_plugin.WindowCommand):

    def get_git_repository(self):
        # Get the folder of the current view
        dirs = [os.path.dirname(self.window.active_view().file_name())] if self.window.active_view() and self.window.active_view().file_name() else []

        # Get get windows folders
        dirs += [f for f in self.window.folders()]

        # Detect folders of open views
        dirs += [os.path.dirname(view.file_name()) for view in self.window.views() if view and view.file_name()]

        # Check for git folder
        for dir_path in list(set(dirs)):
            git_dir = os.path.join(dir_path, '.git')
            if os.path.exists(git_dir):
                return git_dir

    def run(self, cmd):
        s = sublime.load_settings("Git GUI Clients.sublime-settings")

        # Get repository location and git gui client
        repository = self.get_git_repository()
        excecutable = s.get(cmd)
        if repository and excecutable:
            print("Git GUI Clients:", excecutable, repository)
            p = subprocess.Popen(excecutable, cwd=repository, shell=True)
