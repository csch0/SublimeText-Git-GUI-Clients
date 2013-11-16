import sublime
import sublime_plugin

import os
import shutil
import subprocess


class GgcOpenCommand(sublime_plugin.WindowCommand):

    def get_git_repository(self):
        # Get the folder of the current view
        dirs = [os.path.dirname(self.window.active_view().file_name())] if self.window.active_view() and self.window.active_view().file_name() else []

        # Get get windows folders
        dirs += [f for f in self.window.folders()]

        # Check for git folder
        for dir_path in list(set(dirs)):
            git_dir = os.path.join(dir_path, '.git')
            if os.path.exists(git_dir):
                return git_dir

    def get_excecutable(self, cmd):        
        s = sublime.load_settings("Git GUI Clients.sublime-settings")
        for excecutable in s.get(cmd):
            if os.path.exists(excecutable):
                return excecutable

        # Fallback search on path
        return shutil.which(os.path.basename(s.get(cmd)[0])) if s.get(cmd) else None

    def is_enabled(self, cmd):
        return self.get_excecutable(cmd) != None

    def run(self, cmd):
        # Get repository location and git gui client
        excecutable = self.get_excecutable(cmd)
        repository = self.get_git_repository()
        if repository and excecutable:
            print("Git GUI Clients:", excecutable, repository)
            p = subprocess.Popen(excecutable, cwd=repository, shell=True)
