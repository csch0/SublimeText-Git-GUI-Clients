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

        # Detect folders of open views
        dirs += [os.path.dirname(view.file_name()) for view in self.window.views() if view and view.file_name()]

        # preserve order of folders, from
        # http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order
        def customSet(seq):
            seen = set()
            seen_add = seen.add
            return [ x for x in seq if not (x in seen or seen_add(x))]

        # Check for git folder
        for dir_path in list(customSet(dirs)):

            # search for git folder
            while dir_path:
                if os.path.exists(os.path.join(dir_path, '.git')):
                    return dir_path

                parent = os.path.realpath(os.path.join(dir_path, os.path.pardir))
                if parent == dir_path:
                    break
                dir_path = parent

    def get_excecutable(self, cmd):
        s = sublime.load_settings("Git GUI Clients.sublime-settings")
        for excecutable in s.get(cmd):
            if os.path.exists(excecutable):
                return excecutable

        # Fallback search on path
        return shutil.which(os.path.basename(s.get(cmd)[0])) if s.get(cmd) else None

    def is_enabled(self, cmd):
        return True if self.get_excecutable(cmd) else False

    def run(self, cmd):
        # Get repository location and git gui client
        excecutable = self.get_excecutable(cmd)
        repository = self.get_git_repository()

        if not excecutable:
            print("Git GUI Clients: No GUI executable exists on the computer. Check path configs.")
            return

        if not repository:
            print("Git GUI Clients: File/project is not in a Git repo.")
            return

        print("Git GUI Clients:", excecutable, repository)
        subprocess.Popen(excecutable, cwd=repository, shell=True)
