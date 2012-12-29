#import sublime
import sublime_plugin


class Laynger(sublime_plugin.TextCommand):
    def run(self, edit, opt='default'):
        window = self.view.window()

        layout = window.get_layout()

        # support only 2 columns
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
