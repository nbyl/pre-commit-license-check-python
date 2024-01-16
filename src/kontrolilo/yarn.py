# -*- coding: utf-8 -*-
import csv
from subprocess import run
from typing import List

from kontrolilo.base_checker import BaseLicenseChecker
from kontrolilo.shared_main import shared_main
from kontrolilo.configuration.package import Package


class YarnLicenseChecker(BaseLicenseChecker):
    def prepare_directory(self, directory: str):
        run('yarn install', capture_output=True, check=True, cwd=directory, shell=True)

    def get_license_checker_command(self, directory: str) -> str:
        # yes, we are using csv here. license-checker's json output does not build an array of licenses, which is
        # pretty hard to parse.
        return 'npx license-checker --csv'

    def parse_packages(self, output: str, configuration: dict, directory: str) -> List[Package]:
        packages = []
        package_reader = csv.DictReader(output.splitlines())
        for row in package_reader:
            module = row['module name']
            name = module
            version = module
            index = module.find('@')
            if index > 0:
                name = module[:index]
                version = module[index + 1:]

            packages.append(Package(name, version, row['license']))
            print(packages)

        return packages


def main():
    shared_main(YarnLicenseChecker())


if __name__ == '__main__':
    main()
