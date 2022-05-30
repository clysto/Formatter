import sublime
import sublime_plugin

from .formatters.clangformat import ClangformatFormatter
from .formatters.black import BlackFormatter
from .formatters.prettier import PrettierFormatter
from .formatters.latexindent import LatexindentFormatter
from .formatters.common import FormatException


FORMATTERS = {
    "C": ClangformatFormatter,
    "C++": ClangformatFormatter,
    "Python": BlackFormatter,
    "JavaScript": PrettierFormatter,
    "JavaScript (Babel)": PrettierFormatter,
    "JSON": PrettierFormatter,
    "HTML": PrettierFormatter,
    "YAML": PrettierFormatter,
    "CSS": PrettierFormatter,
    "LaTeX": LatexindentFormatter,
    "Vue Component": PrettierFormatter,
}


class FormatCommand(sublime_plugin.TextCommand):
    def get_panel(self):
        window = self.view.window()
        panel = window.find_output_panel("output.formatter")
        if panel is None:
            panel = window.create_output_panel("formatter")
            settings = panel.settings()
            settings.set("line_numbers", False)
            settings.set("gutter", False)
        return panel

    def run(self, edit):
        window = self.view.window()
        region = sublime.Region(0, self.view.size())
        text = self.view.substr(region)
        syntax = self.view.syntax()
        filename = self.view.sheet().file_name()
        panel = self.get_panel()
        if self.view.is_read_only() or len(text) == 0 or syntax is None:
            return
        if syntax.name in FORMATTERS:
            formatter = FORMATTERS[syntax.name](syntax.name, filename)
            try:
                result = formatter.format(text)
                self.view.replace(edit, region, result)
                window.run_command("hide_panel", {"panel": "output.formatter"})
                sublime.status_message("Formated {}".format(filename))
            except FormatException as e:
                panel.run_command("insert", {"characters": e.stderr})
                window.run_command("show_panel", {"panel": "output.formatter"})
        else:
            sublime.status_message("No available formatter.")
