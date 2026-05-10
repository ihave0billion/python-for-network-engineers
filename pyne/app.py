"""Textual TUI shell: lesson list (left) + rendered markdown (right)."""
from __future__ import annotations

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.widgets import Footer, Header, Label, ListItem, ListView, Markdown

from pyne.lessons import Lesson
from pyne.progress import load_progress, save_progress


class PyneApp(App):
    CSS = """
    Screen { layout: vertical; }
    #body { layout: horizontal; height: 1fr; }
    #lesson_list { width: 40; border-right: solid $accent; }
    #lesson_content { padding: 1 2; }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("n", "next_lesson", "Next"),
        Binding("p", "prev_lesson", "Prev"),
        Binding("m", "toggle_complete", "Mark done"),
    ]

    def __init__(self, lessons: list[Lesson]) -> None:
        super().__init__()
        self.lessons = lessons
        self.progress = load_progress()
        self.current_index = self._resume_index()

    def _resume_index(self) -> int:
        if self.progress.last_lesson_number is None:
            return 0
        for i, lesson in enumerate(self.lessons):
            if lesson.number == self.progress.last_lesson_number:
                return i
        return 0

    def _list_item(self, lesson: Lesson) -> ListItem:
        marker = "✓" if lesson.number in self.progress.completed else " "
        return ListItem(Label(f"[{marker}] {lesson.number:02d}  {lesson.display_title}"))

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="body"):
            yield ListView(
                *[self._list_item(lesson) for lesson in self.lessons],
                id="lesson_list",
            )
            yield Markdown(id="lesson_content")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "pyne — Python for Network Engineers"
        self.sub_title = f"{len(self.progress.completed)}/{len(self.lessons)} complete"
        list_view = self.query_one(ListView)
        list_view.index = self.current_index
        list_view.focus()
        self._show_lesson(self.current_index)

    def _show_lesson(self, index: int) -> None:
        if not (0 <= index < len(self.lessons)):
            return
        lesson = self.lessons[index]
        markdown = self.query_one("#lesson_content", Markdown)
        try:
            content = lesson.markdown_path.read_text(encoding="utf-8")
        except OSError as exc:
            content = f"# Failed to load lesson\n\n```\n{exc}\n```"
        markdown.update(content)
        self.current_index = index
        self.progress.last_lesson_number = lesson.number
        save_progress(self.progress)

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        if event.list_view.index is not None:
            self._show_lesson(event.list_view.index)

    def action_next_lesson(self) -> None:
        target = min(self.current_index + 1, len(self.lessons) - 1)
        self.query_one(ListView).index = target

    def action_prev_lesson(self) -> None:
        target = max(self.current_index - 1, 0)
        self.query_one(ListView).index = target

    def action_toggle_complete(self) -> None:
        lesson = self.lessons[self.current_index]
        if lesson.number in self.progress.completed:
            self.progress.completed.remove(lesson.number)
            self.notify(f"Lesson {lesson.number:02d} marked incomplete.")
        else:
            self.progress.completed.add(lesson.number)
            self.notify(f"Lesson {lesson.number:02d} marked complete.")
        save_progress(self.progress)
        self._rebuild_list()
        self.sub_title = f"{len(self.progress.completed)}/{len(self.lessons)} complete"

    def _rebuild_list(self) -> None:
        list_view = self.query_one(ListView)
        list_view.clear()
        for lesson in self.lessons:
            list_view.append(self._list_item(lesson))
        list_view.index = self.current_index
