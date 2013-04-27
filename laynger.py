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
        settings = sublime.load_settings(SETTINGS_FILE)

        window = self.view.window()
        layout = window.get_layout()

        if opt == u'1_column':
            if True == settings.get('keep_groups'):
                self.save_groups()
            window.set_layout(DEFAULT['1_column'])
            return
        elif opt == u'2_columns':
            store = sublime.load_settings(STORE_FILE)
            if True == settings.get('keep_layout') and store.has('2_columns'):
                window.set_layout(store.get('2_columns'))
            else:
                window.set_layout(DEFAULT['2_columns'])
            if True == settings.get('keep_groups') and store.has('groups'):
                self.restore_groups()

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

        if True == settings.get('keep_layout'):
            self.save_layout()

    def save_layout(self):
        settings = sublime.load_settings(SETTINGS_FILE)
        store = sublime.load_settings(STORE_FILE)
        window = self.view.window()

        layout = window.get_layout()
        ncolumns = len(layout['cols']) - 1
        if ncolumns == 2:
            store.set("2_columns", layout)

        if True == settings.get('keep_groups'):
            self.save_groups()

    def save_groups(self):
        store = sublime.load_settings(STORE_FILE)
        window = self.view.window()

        groups = {'num_groups': window.num_groups(), 'files': {}}
        for group_id in range(0, window.num_groups()):
            views = window.views_in_group(group_id)
            i = 0
            for v in views:
                f = v.file_name()
                k = str(group_id) + '-' + str(i)
                groups['files'][k] = f
                i+=1

        store.set('groups', groups)

        sublime.save_settings(STORE_FILE)

    def restore_groups(self):
        window = self.view.window()
        views = window.views()

        store = sublime.load_settings(STORE_FILE)
        groups = store.get('groups')

        active_file = window.active_view().file_name()

        last_view_in_group = [0 for i in range(0, groups['num_groups'])]

        used_keys = {}
        used_views = {}
        for view in window.views():
            f = view.file_name()
            for k in groups['files']:
                if used_keys.has_key(k):
                    continue
                if used_views.has_key(str(view)):
                    continue
                group_id = int(k.split('-')[0])
                stored_f = groups['files'][k]
                if stored_f == f:
                    window.set_view_index(view, group_id, last_view_in_group[group_id])
                    last_view_in_group[group_id]+=1
                    used_keys[k] = 1
                    used_views[str(view)] = 1

        for v in views:
            f = v.file_name()
            if f == active_file:
                window.focus_view(v)
        return
