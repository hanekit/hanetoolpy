import typer

import inspect
from typing import Union, Iterable

import click
from rich.console import group
from rich.markdown import Markdown
from rich.text import Text
from typer.core import MarkupMode
from typer.rich_utils import DEPRECATED_STRING, STYLE_DEPRECATED, STYLE_HELPTEXT_FIRST_LINE, MARKUP_MODE_MARKDOWN, \
    MARKUP_MODE_RICH, _make_rich_rext, STYLE_HELPTEXT


@group()
def get_custom_help_text(
        *,
        obj: Union[click.Command, click.Group],
        markup_mode: MarkupMode,
) -> Iterable[Union[Markdown, Text]]:
    """Build primary help text for a click command or group.

    Returns the prose help text for a command or group, rendered either as a
    Rich Text object or as Markdown.
    If the command is marked as deprecated, the deprecated string will be prepended.
    """
    # Prepend deprecated status
    if obj.deprecated:
        yield Text(DEPRECATED_STRING, style=STYLE_DEPRECATED)

    # Fetch and dedent the help text
    help_text = inspect.cleandoc(obj.help or "")

    # Trim off anything that comes after \f on its own line
    help_text = help_text.partition("\f")[0]

    # Get the first paragraph
    first_line = help_text.split("\n\n")[0]
    # Remove single linebreaks
    if markup_mode != MARKUP_MODE_MARKDOWN and not first_line.startswith("\b"):
        first_line = first_line.replace("\n", " ")
    yield _make_rich_rext(
        text=first_line.strip(),
        style=STYLE_HELPTEXT_FIRST_LINE,
        markup_mode=markup_mode,
    )

    # Add blank line between first paragraph and remaining lines
    if len(help_text.split("\n\n")) > 1:
        yield ""  # ADD THIS

    # Get remaining lines, remove single line breaks and format as dim
    remaining_paragraphs = help_text.split("\n\n")[1:]
    if remaining_paragraphs:
        if markup_mode != MARKUP_MODE_RICH:
            # Remove single linebreaks
            remaining_paragraphs = [
                x.replace("\n", " ").strip()
                if not x.startswith("\b")
                else "{}\n".format(x.strip("\b\n"))
                for x in remaining_paragraphs
            ]
            # Join back together
            remaining_lines = "\n".join(remaining_paragraphs)
        else:
            # Join with double linebreaks if markdown
            remaining_lines = "\n\n".join(remaining_paragraphs)

        yield _make_rich_rext(
            text=remaining_lines,
            style=STYLE_HELPTEXT,
            markup_mode=markup_mode,
        )
