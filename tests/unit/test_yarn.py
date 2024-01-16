# -*- coding: utf-8 -*-
from tempfile import TemporaryDirectory
from unittest.mock import patch, call

from kontrolilo.configuration import Configuration
from kontrolilo.configuration.package import Package
from kontrolilo.npm import NpmLicenseChecker


class TestNpmLicenseChecker:
    DEMO_LICENSE_OUTPUT = \
        '''"module name","license","repository"
"xtend@4.0.2","MIT","https://github.com/Raynos/xtend"
"y18n@4.0.0","ISC","https://github.com/yargs/y18n"
"y18n@5.0.5","ISC","https://github.com/yargs/y18n"'''

    def setup(self):
        self.directory = TemporaryDirectory()
        self.checker = YarnLicenseChecker()

    @patch('kontrolilo.yarn.run')
    def test_prepare_directory(self, run_mock):
        run_mock.return_value = {}

        with TemporaryDirectory() as directory:
            self.checker.prepare_directory(directory)
            run_mock.assert_has_calls([
                call('yarn install', capture_output=True, check=True, cwd=directory, shell=True),
            ])

    def test_get_license_checker_command(self):
        assert self.checker.get_license_checker_command('') == 'npx license-checker --csv'

    def test_parse_packages(self):
        packages = self.checker.parse_packages(self.DEMO_LICENSE_OUTPUT, Configuration(
            allowed_licenses=[],
            excluded_packages=[]
        ), self.directory.name)
        assert packages == [
            Package('xtend', '4.0.2', 'MIT'),
            Package('y18n', '4.0.0', 'ISC'),
            Package('y18n', '5.0.5', 'ISC'),

        ]
