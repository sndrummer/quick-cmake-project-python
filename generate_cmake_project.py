#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Create a C++ Cmake Project from a template"""
import argparse
import os
import subprocess
from git import Repo
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("project_name", help="The project name")
args = parser.parse_args()

cwd = os.getcwd()
project_name = args.project_name.lower()
# use underscores since cmake seems to like that
project_name = project_name.replace(" ", "-")
project_name = project_name.replace("_", "-")
repo_dir = os.path.join(cwd, project_name)
TEMPLATE_URL = "https://github.com/sndrummer/cmake_cpp_basic_template.git"


def pull_template():
    print("Getting template from {}...".format(TEMPLATE_URL))
    if os.path.isdir(repo_dir):
        exit("FAILURE: Directory {} already exists, exiting...".format(project_name))
    Repo.clone_from(TEMPLATE_URL, repo_dir)
    if not os.path.isdir(repo_dir):
        exit("FAILURE: failed to clone cmake template")


def modify_cmakelists():
    print("Configuring project for CMake...")
    print(
        "--------------------------------------------------------------------------------------------"
    )
    cmake_lists_file = os.path.join(repo_dir, "CMakeLists.txt")
    with open(cmake_lists_file) as f:
        lines = f.readlines()

    # Set the correct cmake project name, (cmake likes underscores)
    project_name_cmake = project_name.replace("-", "_")
    lines[0] = lines[0].replace("@PROJECT_NAME@", project_name_cmake)
    with open(cmake_lists_file, "w") as f:
        f.writelines(lines)

    # Remove the .git/ of the template
    git_dir = os.path.join(repo_dir, ".git")
    if os.path.isdir(git_dir):
        shutil.rmtree(git_dir)


def setup_project():
    # Run cmake setup
    os.chdir(repo_dir)
    build_dir_path = os.path.join(repo_dir, "build")
    if not os.path.isdir(build_dir_path):
        exit("FAILURE: no build directory at {}".format(build_dir_path))
    os.chdir(build_dir_path)
    return_code = subprocess.run(
        [
            "cmake",
            "-DCMAKE_C_COMPILER=/usr/bin/gcc",
            "-DCMAKE_CXX_COMPILER=/usr/bin/g++",
            "..",
        ]
    ).returncode

    if return_code != 0:
        exit("FAILURE: CMake configuration failed, exiting...")
    os.chdir(repo_dir)
    # Now git init the repo
    Repo.init(repo_dir)


def main():
    pull_template()
    modify_cmakelists()
    setup_project()
    print(
        "--------------------------------------------------------------------------------------------"
    )
    print("Success! Project created at {}".format(repo_dir))


if __name__ == "__main__":
    main()
