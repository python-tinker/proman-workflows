# copyright: (c) 2021 by Jesse Johnson.
# license: AGPL-3.0-or-later, see LICENSE for more details.
"""Provide convenience tool to manage projects with Python."""

import logging
import os
from dataclasses import asdict
from pprint import pprint  # noqa
from typing import List

from invoke import Program
from proman_common.config import Config
from proman_common.filepaths import AppDirs

from workflows import (
    container,
    docs,
    exception,
    formatter,
    init,
    package,
    qa,
    sca,
    stlc,
    utils,
)
from workflows.collection import Collection
from workflows.config import (  # WorkflowConfig,
    DocsConfig,
    ProjectConfig,
    ProjectDirs,
)

__author__ = 'Jesse P. Johnson'
__author_email__ = 'jpj6652@gmail.com'
__title__ = 'workflows'
__description__ = 'Convenience module to manage project tools with Python.'
__version__ = '0.1.0a7'
__license__ = 'AGPL-3.0-or-later'
__copyright__ = 'Copyright 2021 Jesse Johnson.'

logging.getLogger(__name__).addHandler(logging.NullHandler())


class WorkflowProgram(Program):
    """Provide workflow integration with invoke program."""

    def parse_collection(self) -> None:
        """Patch collection parse to load project config."""
        if self.namespace is not None:
            self.config.set_project_location(os.getcwd())
            self.config.load_project()
        super().parse_collection()


def get_specfile(project_dir: str, specfiles: List[str]) -> Config:
    """Get source tree from path."""
    for specfile in specfiles:
        filepath = os.path.join(project_dir, specfile)
        if os.path.isfile(filepath):
            config = Config(filepath=filepath)
            config.combine(config.retrieve('.tool.proman.workflows'))
            return config
    raise exception.PromanWorkflowException('no configuration found')


app_dirs = AppDirs(project_name='workflows')
project_dirs = ProjectDirs()
docs_config = DocsConfig()
specfile = get_specfile(
    project_dir=project_dirs.project_dir,
    specfiles=project_dirs.specfiles,
)
project_config = ProjectConfig(
    docs=asdict(docs_config),
    specfile=specfile.data,
    # plugins=specfile.retrieve('.tool.proman.workflows.plugins') or [],
)
# pprint(asdict(project_config))

workflow_namespace = Collection()
workflow_namespace.configure(
    {
        'dirs': asdict(app_dirs),
        'spec': specfile.data,
        'docs': asdict(docs_config),
        # 'working_dir': config.working_dir,
        # 'container_runtime': config.container_runtime,
        **asdict(project_dirs),
    }
)
workflow_namespace.add_collection(container.namespace, name='container')
workflow_namespace.add_collection(docs.namespace, name='docs')
workflow_namespace.add_collection(formatter.namespace, name='style')
workflow_namespace.add_collection(package.namespace, name='dist')
workflow_namespace.add_collection(qa.namespace, name='qa')
workflow_namespace.add_collection(sca.namespace, name='sca')
workflow_namespace.add_collection(utils.namespace, name='utils')
workflow_tools = Program(
    version=__version__,
    namespace=workflow_namespace,
    name=__title__,
    binary='workflow-tools',
    binary_names=['workflow-tools'],
)

workflow_namespace = Collection().from_module(stlc)
workflow_namespace.configure(
    {
        **asdict(app_dirs),
        **specfile,
        # **asdict(project_config),
    }
)
# workflow_namespace.load_collections(plugins=asdict(project_config)['plugins'])
workflow_namespace.add_collection(init.namespace, name='init')
workflow = WorkflowProgram(
    name=__title__,
    namespace=workflow_namespace,
    binary='workflow',
    binary_names=['workflow'],
    # config_class=WorkflowConfig,
    version=__version__,
)

__all__ = ['workflow', 'tools']
