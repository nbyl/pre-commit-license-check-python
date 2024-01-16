# -*- coding: utf-8 -*-
from pathlib import Path
from shutil import copy
from typing import List

from tests.integration.base_integration_test import IntegrationTestBase


class TestNpmCheck(IntegrationTestBase):

    def prepare_test_directory(self):
        copy(Path(Path(__file__).parent, 'package.json').absolute(),
             Path(self.directory.name, 'package.json').absolute())

    def get_hook_id(self) -> str:
        return 'license-check-npm'

    def get_allowed_licenses(self) -> List[str]:
        return ['ISC', 'MIT']
