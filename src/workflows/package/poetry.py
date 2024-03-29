"""Publish packages using Poetry."""

from typing import TYPE_CHECKING, List, Optional

from invoke import Collection, task

if TYPE_CHECKING:
    from invoke import Context


@task
def requirements(
    ctx,  # type: Context
    output='requirements.txt',  # type: str
    dev=False,  # type: bool
    extras=None,  # type: Optional[List[str]]
):  # type: (...) -> None
    """Generate requirements file."""
    args = ['--format requirements.txt', f"--output {output}"]
    if dev:
        args.append('--dev')
    if extras is not None:
        args.append(f"--extras {','.join(extras)}")
    ctx.run(f"poetry export {' '.join(args)}")


# XXX: use `python -m build` instead
@task
def build(ctx, kind=None):  # type: (Context, Optional[bool]) -> None
    """Build wheel package."""
    args = ['--no-interaction']
    if kind:
        args.append(f"--format={kind}")
    ctx.run(f"poetry build {' '.join(args)}")


@task
def install(
    ctx,  # type: Context
    dev=True,  # type: bool
    editable=True,  # type: bool
    remove_untracked=False,  # type: bool
    extras=None,  # type: Optional[str]
):  # type: (...) -> None
    """Install project into local environment."""
    args = ['--no-interaction']
    if not dev:
        args.append('--no-dev')
    if not editable:
        args.append('--no-root')
    if remove_untracked:
        args.append('--remove-untracked')
    if extras:
        args.append(f"--extras={extras}")
    ctx.run(f"poetry install {' '.join(args)}")


@task
def publish(
    ctx,  # type: Context
    repository=None,  # type: Optional[str]
    username=None,  # type: Optional[str]
    password=None,  # type: Optional[str]
    cert_path=None,  # type: Optional[str]
    client_cert_path=None,  # type: Optional[str]
):  # type: (...) -> None
    """Publish package to a PyPI repository."""
    args = ['--no-interaction']
    # TODO: check if credentials exist run setup otherwise
    if repository:
        args.append(f"--repository={repository}")
    if username:
        args.append(f"--username={username}")
        if password:
            args.append(f"--password='{password}'")
        else:
            raise Exception('username requires a password')
    if cert_path:
        args.append(f"--cert={cert_path}")
    if client_cert_path:
        args.append(f"--client-cert={client_cert_path}")
    ctx.run(f"poetry publish {' '.join(args)}")


namespace: Collection = Collection(build, install, publish)
