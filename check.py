import sublime, sublime_plugin

class CheckCommand(sublime_plugin.TextCommand):

    CHECK_REGIONS_KEY = '-checkstyle'
    def sel_and_go(self, region):
        assert region
        self.view.show_at_center(region)
    
    def mark_all(self, regions):
        assert regions
        self.view.add_regions(CheckCommand.CHECK_REGIONS_KEY, regions, 'string', '', sublime.PERSISTENT)

    WRONG_STYLEs = '|'.join((
                    r'(^\s*?\n){2,}', 
                    r'\b(if|switch|for|foreach)\(', 
                    r'\w\s{2,}=|=\s{2,}\w',
                    r'\w,\S'
                    ))

    def run(self, edit):
        rgs = self.view.get_regions(CheckCommand.CHECK_REGIONS_KEY)
        rs = self.view.find_all(CheckCommand.WRONG_STYLEs)
        if rs:
            self.mark_all(rs)
            if not rgs:
                self.sel_and_go(rs[0])
            return

class ClearcheckCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.view.erase_regions(CheckCommand.CHECK_REGIONS_KEY)
        return;

class Onmodify(sublime_plugin.EventListener):

    def on_modified(self, view):
        rgs = view.get_regions(CheckCommand.CHECK_REGIONS_KEY)
        if not rgs:
            return;
        view.run_command('check')
