# copyright: (c) 2020 by Jesse Johnson.
# license: AGPL-3.0-or-later, see LICENSE for more details.
"""Quality Assurance Task-Runner."""

from typing import TYPE_CHECKING

from invoke import Collection, task

if TYPE_CHECKING:
    from invoke import Context


@task(name='format')
def style(ctx):  # type: (Context) -> None
    """Format project source code to PEP8 standard."""
    ctx.run(f"autopep8 --in-place --recursive {ctx.project_dir}")


namespace = Collection(style)
