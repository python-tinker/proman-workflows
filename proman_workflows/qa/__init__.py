# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Quality Assurance Task-Runner."""

import logging

from proman_workflows.collection import Collection

logging.getLogger(__name__).addHandler(logging.NullHandler())

# Assemble collections for namespace
namespace = Collection()
namespace.configure(
    {
        '_collections': [
            {
                'name': 'sort-headers',
                'driver_name': 'isort',
                'driver_namespace': 'proman.workflow.formatter',
            }, {
                'name': 'format',
                'driver_name': 'black',
                'driver_namespace': 'proman.workflow.formatter',
            }, {
                'name': 'typing',
                'driver_name': 'mypy',
                'driver_namespace': 'proman.workflow.typing',
             }, {
                 'name': 'lint',
                 'driver_name': 'flake8',
                 'driver_namespace': 'proman.workflow.lint',
             }, {
                 'name': 'unit-tests',
                 'driver_name': 'pytest',
                 'driver_namespace': 'proman.workflow.unit_tests',
             }
        ]
    }
)
namespace.load_collections()

__all__ = [
    'namespace',
]