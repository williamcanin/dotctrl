from os.path import exists, join
from sys import exit, platform
from textwrap import dedent

from snakypy.helpers import FG, printer
from snakypy.helpers.checking import whoami
from snakypy.helpers.files import create_file, create_json
from snakypy.helpers.path import create as create_path
from snakypy.helpers.subprocess import super_command

from snakypy.dotctrl import __info__
from snakypy.dotctrl.config import config, gitignore, readme
from snakypy.dotctrl.config.base import Base
from snakypy.dotctrl.utils import git_init_command


class InitCommand(Base):
    def __init__(self, root, home):
        Base.__init__(self, root, home)

    def main(self, arguments: dict) -> None:
        """Base repository method."""
        # print(self.ROOT)
        # exit(0)

        init_auto = False

        if exists(self.config_path):
            printer("Repository is already defined.", foreground=FG().FINISH)
            exit(0)

        if not arguments["--auto"]:
            create_path(self.repo_path)
            create_json(config.content, self.config_path, force=True)
            create_file(readme.content, self.readme, force=True)

        if arguments["--git"]:
            git_init_command()
            create_file(gitignore.content, self.gitignore_path, force=True)
        elif arguments["--auto"]:
            paths = ("/home", "linux") if platform == "linux" else ("/Users", "macos")
            path_current = join(paths[0], ".dotfiles", paths[1])
            if exists(join(path_current, __info__["config"])):
                dir_ = f"{FG().BLUE}{path_current}{FG().YELLOW}"
                printer(
                    f'{__info__["name"]} is already configured in this directory "{dir_}"',
                    foreground=FG().WARNING,
                )
                exit(0)
            message_initial = dedent(
                f"""
            [ATTENTION!]
            You need to have superuser permission on your machine to proceed with this step and create
            an automatic repository with {__info__["name"]}. You can approach the operation by
            pressing Ctrl + C.

            NOTE: The {__info__['name']} directory will be created in: "{FG().BLUE}{path_current}{FG().YELLOW}".
            """
            )
            printer(message_initial, foreground=FG().YELLOW)
            printer("[ Enter superuser password ]", foreground=FG().QUESTION)
            whoami_user = whoami()
            super_scripts = f"""
            mkdir -p {join(paths[0], '.dotfiles', paths[1])};
            chown -R {whoami_user} {join(paths[0], '.dotfiles')};
            chmod -R 700 {join(paths[0], '.dotfiles')};"""
            sp = super_command(super_scripts)
            if sp is None:
                exit(0)

            create_path(self.repo_path)
            create_json(config.content, self.config_path, force=True)
            create_file(readme.content, self.readme, force=True)

            printer(
                f"Initialized {__info__['name']} repository in {join(paths[0], '.dotfiles', paths[1])}",
                foreground=FG().FINISH,
            )
            init_auto = True

        if not init_auto:
            printer(
                f"Initialized {__info__['name']} repository in {self.repo_path}",
                foreground=FG().FINISH,
            )
