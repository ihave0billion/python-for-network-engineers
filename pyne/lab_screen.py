"""Lab screen: render README + script preview, run the lab, show output."""
from __future__ import annotations

from pathlib import Path

from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button, Footer, Label, Markdown

from pyne.config import CMLConfig
from pyne.lab_runner import LabResult, find_primary_script, run_lab
from pyne.lessons import Lesson


class LabScreen(Screen[None]):
    CSS = """
    ScrollableContainer { padding: 1 2; }
    #title { text-style: bold; color: $accent; margin-bottom: 1; }
    .section { text-style: bold underline; margin-top: 1; }
    .actions { height: auto; margin: 1 0; }
    Button { margin-right: 2; }
    #output { margin-top: 1; }
    """

    BINDINGS = [
        Binding("escape", "back", "Back"),
        Binding("ctrl+r", "run", "Run lab"),
    ]

    def __init__(self, lesson: Lesson, config: CMLConfig | None) -> None:
        super().__init__()
        self.lesson = lesson
        self.config = config
        assert lesson.lab_path is not None, "LabScreen requires a lesson with a lab"
        self.lab_path: Path = lesson.lab_path

    def compose(self) -> ComposeResult:
        with ScrollableContainer():
            yield Label(
                f"Lesson {self.lesson.number:02d} — Lab",
                id="title",
            )

            yield Label("Lab notes", classes="section")
            yield Markdown(self._readme_markdown(), id="readme")

            yield Label("Primary script", classes="section")
            yield Markdown(self._script_markdown(), id="script")

            yield Horizontal(
                Button("Run lab (^R)", id="run", variant="primary"),
                Button("Back (Esc)", id="back"),
                classes="actions",
            )

            yield Label("Output", classes="section")
            yield Markdown(
                "_Press Run to execute the lab._", id="output"
            )
        yield Footer()

    def _readme_markdown(self) -> str:
        readme = self.lab_path / "README.md"
        if not readme.exists():
            return f"_No README in {self.lab_path.name}._"
        try:
            return readme.read_text(encoding="utf-8")
        except OSError as exc:
            return f"_Failed to read README:_ {exc}"

    def _script_markdown(self) -> str:
        script = find_primary_script(self.lab_path)
        if script is None:
            return "_No Python script found in this lab folder._"
        try:
            source = script.read_text(encoding="utf-8")
        except OSError as exc:
            return f"_Failed to read {script.name}:_ {exc}"
        return f"`{script.name}`\n\n```python\n{source}```"

    def action_back(self) -> None:
        self.dismiss(None)

    def action_run(self) -> None:
        self._trigger_run()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "run":
            self._trigger_run()
        elif event.button.id == "back":
            self.dismiss(None)

    def _trigger_run(self) -> None:
        self.query_one("#output", Markdown).update("_Running…_")
        self._run_worker()

    @work(exclusive=True, thread=True)
    def _run_worker(self) -> None:
        result = run_lab(self.lab_path, self.config)
        self.app.call_from_thread(self._show_result, result)

    def _show_result(self, result: LabResult) -> None:
        parts: list[str] = []
        if result.simulated:
            parts.append(f"**[SIMULATED]** — {result.reason}")
        else:
            parts.append(f"**Live output** — {result.reason}")

        body = result.output if result.output.strip() else "_(no output)_"
        parts.append(f"```\n{body}\n```")

        if result.real_stderr.strip():
            parts.append(
                "Real-run stderr (kept for debugging):\n\n"
                f"```\n{result.real_stderr}\n```"
            )

        self.query_one("#output", Markdown).update("\n\n".join(parts))
