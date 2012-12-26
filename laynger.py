#import sublime
import sublime_plugin


class laynger(sublime_plugin.TextCommand):
    def run(self, edit, opt='center'):
        window = self.view.window()

        layout = window.get_layout()

        if len(layout['cols']) != 3:
            return

        if opt == u'center':
            layout['cols'][1] = 0.5
        elif opt == u'right':
            if layout['cols'][1] < 0.99:
                layout['cols'][1] += 0.01
        else:
            if layout['cols'][1] > 0.01:
                layout['cols'][1] -= 0.01

        window.run_command('set_layout', layout)
