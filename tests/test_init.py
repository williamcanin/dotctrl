from os.path import exists

from snakypy.dotctrl.actions.init import InitCommand
from snakypy.dotctrl.actions.repo import RepoCommand

from .utilities import Basic, fixture  # noqa: E261, F401


class InitTester(Basic):
    def __init__(self, fixt):  # noqa: F811
        Basic.__init__(self, fixt)

    @property
    def args(self):
        return self.menu.args(argv=["init"])

    def repo_check(self, value):
        return self.menu.args(argv=["repo", "--check"])

    def run(self):

        output = RepoCommand(self.root, self.home).main(self.repo_check)

        if output["code"] != "28":
            assert False

        output = InitCommand(self.root, self.home).main(self.args)

        if not exists(self.base.config_path):
            assert False

        if not exists(self.base.repo_path):
            assert False

        if output["code"] != "10":
            assert False


def test_init(fixture):  # noqa: F811
    init = InitTester(fixture)
    init.run()
