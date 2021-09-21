# -*- coding: utf-8 -*-
# copyright: (c) 2021 by Jesse Johnson.
# license: MPL-2.0, see LICENSE for more details.
"""Provide convenience tool to manage projects with Python."""

import logging
import os
from typing import List

from invoke import Program
from proman_common.config import Config

from proman_workflows import (
    config, docs, exception, package, qa, security, utils
)
from proman_workflows.collection import Collection
# from proman_workflows.vcs import Git

__author__ = 'Jesse P. Johnson'
__author_email__ = 'jpj6652@gmail.com'
__title__ = 'proman-workflows'
__description__ = 'Convenience module to manage project tools with Python.'
__version__ = '0.1.0'
__license__ = 'MPL-2.0'
__copyright__ = 'Copyright 2021 Jesse Johnson.'

logging.getLogger(__name__).addHandler(logging.NullHandler())


def get_specfile(
    basepath: str = os.getcwd(),
    filenames: List[str] = config.filenames,
) -> Config:
    """Get source tree from path."""
    for filename in filenames:
        filepath = os.path.join(basepath, filename)
        if os.path.isfile(filepath):
            return Config(filepath=filepath)
    raise exception.PromanWorkflowException('no configuration found')


specfile = get_specfile()

workflow_namespace = Collection()
workflow_namespace.configure(
    {
        'spec': specfile.data,
        'working_dir': config.working_dir,
    }
)
#         '_collections': [
#              {
#                 'name': 'package',
#                 'driver_name': 'poetry',
#                 'driver_namespace': 'proman.workflow.package'
#              }, {
#                 'name': 'typing',
#                 'driver_name': 'mypy',
#                 'driver_namespace': 'proman.workflow.typing'
#              }, {
#                 'name': 'sast',
#                 'driver_name': 'bandit',
#                 'driver_namespace': 'proman.workflow.sca',
#              }, {
#                  'name': 'dependency-scan',
#                  'driver_name': 'safety',
#                  'driver_namespace': 'proman.workflow.sca'
#              }, {
#                  'name': 'unit-tests',
#                  'driver_name': 'pytest',
#                  'driver_namespace': 'proman.workflow.unit_tests'
#              }
#         ]
#     }
# )
# workflow_namespace.load_collections()
workflow_namespace.add_collection(docs.namespace, name='docs')
workflow_namespace.add_collection(package.namespace, name='dist')
workflow_namespace.add_collection(qa.namespace, name='qa')
workflow_namespace.add_collection(security.namespace, name='sec')
workflow_namespace.add_collection(utils.tasks, name='utils')
workflow = Program(
    version=__version__,
    namespace=workflow_namespace,
    name=__title__,
    binary='workflow',
    binary_names=['workflow'],
)

project_namespace = Collection()
project_namespace.configure(
    {
        'spec': specfile.data,
        '_collections': [
            {
                'name': 'hooks',
                'driver_name': 'git_hooks',
                'driver_namespace': 'proman.workflow.scm',
            }, {
                'name': 'sort-headers',
                'driver_name': 'isort',
                'driver_namespace': 'proman.workflow.formatter'
            }, {
                'name': 'format',
                'driver_name': 'black',
                'driver_namespace': 'proman.workflow.formatter'
            }, {
                'name': 'gpg',
                'driver_name': 'gpg',
                'driver_namespace': 'proman.workflow.pki',
            }, {
                'name': 'tls',
                'driver_name': 'tls',
                'driver_namespace': 'proman.workflow.pki'
            }
        ]
    }
)
project_namespace.load_collections()
project = Program(
    version=__version__,
    namespace=project_namespace,
    name=__title__,
    binary='project',
    binary_names=['project'],
)

__all__ = [
    'project',
    'workflow',
]
