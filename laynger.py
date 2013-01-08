import sublime
import sublime_plugin

SETTINGS_FILE = 'laynger.sublime-settings'
STORE_FILE = 'laynger_store.sublime-settings'
DEFAULT = {
    '1_column':   {"cols": [0.0, 1.0], "rows": [0.0, 1.0], "cells": [[0, 0, 1, 1]]},
    '2_columns':  {"cols": [0.0, 0.5, 1.0], "rows": [0.0, 1.0], "cells": [[0, 0, 1, 1], [1, 0, 2, 1]]}
}


class laynger(sublime_plugin.TextCommand):
    def run(self, edit, opt='default'):
        #settings = sublime.load_settings(SETTINGS_FILE)
        window = self.view.window()
        layout = window.get_layout()

        if opt == u'1_column':
            window.set_layout(DEFAULT['1_column'])
            return
        elif opt == u'2_columns':
            store = sublime.load_settings(STORE_FILE)
            window.set_layout(store.get('2_columns'))
            return

        if len(layout['cols']) != 3:
            return

        if opt == u'default':
            layout['cols'][1] = 0.5
        elif opt == u'right':
            if layout['cols'][1] < 0.99:
                layout['cols'][1] += 0.01
        else:
            if layout['cols'][1] > 0.01:
                layout['cols'][1] -= 0.01

        window.run_command('set_layout', layout)

        self.save_layout()

    def save_layout(self):
        store = sublime.load_settings(STORE_FILE)

        layout = self.view.window().get_layout()
        ncolumns = len(layout['cols']) - 1
        if ncolumns == 2:
            store.set("2_columns", layout)

        sublime.save_settings(STORE_FILE)
