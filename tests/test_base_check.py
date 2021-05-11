# -*- coding: utf-8 -*-
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List
from unittest.mock import patch, Mock

from license_checks.base_checker import BaseLicenseChecker
from license_checks.configuration import Configuration
from license_checks.package import Package


class SimpleLicenseChecker(BaseLicenseChecker):

    def prepare_directory(self, directory: str):
        pass

    def get_license_checker_command(self) -> str:
        return "echo 'Hello World!'"

    def parse_packages(self, output: str, configuration: dict) -> List[Package]:
        return []


class TestBaseLicenseChecker:
    checker: SimpleLicenseChecker

    def setup(self):
        self.checker = SimpleLicenseChecker()

    def test_remove_duplicates(self):
        list = ['a', 'b', 'c', 'a', 'c']
        consolidated_list = self.checker.remove_duplicates(list)
        assert consolidated_list == ['a', 'b', 'c']

    def test_consolidate_directories(self):
        filenames = ['Pipfile.lock', 'Pipfile',
                     'deployment/Pipfile', 'deployment/Pipfile.lock']
        directories = self.checker.consolidate_directories(filenames)
        assert len(directories) == 2
        assert directories == [str(Path('.').absolute()),
                               str(Path('.', 'deployment').absolute())]

    def test_find_invalid_packages(self):
        packages = [
            Package('starlette', '0.14.1', 'BSD License'),
            Package('demo1234', '0.14.1', 'GPL'),
            Package('urllib3', '1.26.4', 'MIT License'),
        ]
        invalid_packages = self.checker.find_invalid_packages(packages, Configuration(
            allowedLicenses=['BSD License', 'MIT License']))
        assert invalid_packages == [Package('demo1234', '0.14.1', 'GPL')]

    def test_print_license_warning(self):
        # this test is mainly run, to verify syntactic correctness
        with TemporaryDirectory() as directory:
            self.checker.print_license_warning(directory, [])

    @patch('license_checks.base_checker.run')
    def test_load_installed_licenses(self, run_mock):
        result_mock = Mock()
        result_mock.configure_mock(**{'stdout': ''})
        run_mock.return_value = result_mock

        with TemporaryDirectory() as directory:
            self.checker.load_installed_packages(directory, {})
            run_mock.assert_called_once_with('echo \'Hello World!\'', capture_output=True, check=True,
                                             cwd=directory, shell=True, text=True)
