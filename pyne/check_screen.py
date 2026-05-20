"""Knowledge-check screen: MCQ + editable code task + result panel."""
from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, ScrollableContainer
from textual.screen import Screen
from textual.widgets import (
    Button,
    Footer,
    Label,
    Markdown,
    RadioButton,
    RadioSet,
    TextArea,
)

from pyne.checks import Check, run_code_task
from pyne.lessons import Lesson


class CheckScreen(Screen[bool]):
    CSS = """
    ScrollableContainer { padding: 1 2; }
    #title { text-style: bold; color: $accent; margin-bottom: 1; }
    .section { text-style: bold underline; margin-top: 1; }
    .prompt { margin-bottom: 1; }
    #code_editor { height: 10; margin-bottom: 1; }
    .actions { height: auto; margin: 1 0; }
    Button { margin-right: 2; }
    #result { margin-top: 1; }
    """

    BINDINGS = [
        Binding("escape", "back", "Back"),
        Binding("ctrl+s", "submit", "Submit"),
        Binding("ctrl+h", "hint", "Hint"),
    ]

    def __init__(self, lesson: Lesson, check: Check) -> None:
        super().__init__()
        self.lesson = lesson
        self.check = check
        self._passed = False

    def compose(self) -> ComposeResult:
        with ScrollableContainer():
            yield Label(
                f"Lesson {self.lesson.number:02d} — {self.check.title}",
                id="title",
            )

            if self.check.mcq is not None:
                yield Label("Multiple-choice", classes="section")
                yield Markdown(self.check.mcq.question, classes="prompt")
                yield RadioSet(
                    *[RadioButton(opt) for opt in self.check.mcq.options],
                    id="mcq_set",
                )

            if self.check.code_task is not None:
                yield Label("Code task", classes="section")
                yield Markdown(self.check.code_task.prompt, classes="prompt")
                yield TextArea.code_editor(
                    text=self.check.code_task.starter,
                    language="python",
                    id="code_editor",
                )

            yield Horizontal(
                Button("Submit & run (^S)", id="submit", variant="primary"),
                Button("Hint (^H)", id="hint"),
                Button("Back (Esc)", id="back"),
                classes="actions",
            )
            yield Markdown("", id="result")
        yield Footer()

    def action_back(self) -> None:
        self.dismiss(self._passed)

    def action_submit(self) -> None:
        self._submit()

    def action_hint(self) -> None:
        self._show_hint()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit":
            self._submit()
        elif event.button.id == "hint":
            self._show_hint()
        elif event.button.id == "back":
            self.dismiss(self._passed)

    def _show_hint(self) -> None:
        hints: list[str] = []
        if self.check.code_task and self.check.code_task.hint:
            hints.append("**Hint**\n\n" + self.check.code_task.hint)
        if not hints:
            hints.append("_No hint provided for this check._")
        self.query_one("#result", Markdown).update("\n\n".join(hints))

    def _submit(self) -> None:
        parts: list[str] = []
        overall_passed = True

        if self.check.mcq is not None:
            mcq_set = self.query_one("#mcq_set", RadioSet)
            choice = mcq_set.pressed_index  # 0-based; -1 if none
            if choice < 0:
                parts.append("**MCQ:** ⚠️ select an option first.")
                overall_passed = False
            elif choice + 1 == self.check.mcq.answer:
                parts.append("**MCQ:** ✓ correct.")
            else:
                parts.append("**MCQ:** ✗ incorrect.")
                overall_passed = False
            if self.check.mcq.explain:
                parts.append(f"> {self.check.mcq.explain}")

        if self.check.code_task is not None:
            code = self.query_one("#code_editor", TextArea).text
            result = run_code_task(
                code, self.check.code_task.expected_stdout_regex
            )
            if result.passed:
                parts.append("**Code task:** ✓ output matched.")
            else:
                parts.append("**Code task:** ✗ output did not match.")
                overall_passed = False
            if result.timed_out:
                parts.append("_Execution timed out._")
            if result.stdout:
                parts.append(f"Stdout:\n```\n{result.stdout}```")
            if result.stderr:
                parts.append(f"Stderr:\n```\n{result.stderr}```")
            if not result.passed and self.check.code_task.hint:
                parts.append(
                    f"Need a nudge? Press **^H** for a hint."
                )

        if overall_passed:
            self._passed = True
            parts.append(
                "---\n**Passed!** Lesson will be marked complete when you press Esc."
            )

        self.query_one("#result", Markdown).update("\n\n".join(parts))
