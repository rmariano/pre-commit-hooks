from __future__ import annotations

import pytest

from pre_commit_hooks.enforce_branch_name import main
from pre_commit_hooks.util import cmd_output
from testing.util import git_commit


@pytest.mark.parametrize("branch_name", ("feature/branch", "bugfix/branch"))
def test_valid_patterns(temp_git_dir, branch_name):
    with temp_git_dir.as_cwd():
        cmd_output("git", "checkout", "-b", branch_name)
        assert main(("--pattern", "feature/.*", "--pattern", "bugfix/.*")) == 0


def test_invalid_branch_name(temp_git_dir):
    with temp_git_dir.as_cwd():
        cmd_output("git", "checkout", "-b", "feature/branch")
        assert main(("--pattern", "bugfix/.*")) == 1


def test_invalid_branch_name_multiple_patterns(temp_git_dir):
    with temp_git_dir.as_cwd():
        cmd_output("git", "checkout", "-b", "invalid-branch-name")
        assert main(("--pattern", "bugfix/.*", "--pattern", "feature/.*")) == 1


def test_not_on_a_branch(temp_git_dir):
    with temp_git_dir.as_cwd():
        git_commit("--allow-empty", "-m1")
        head = cmd_output("git", "rev-parse", "HEAD").strip()
        cmd_output("git", "checkout", head)
        assert main(("--pattern", "foo")) == 1, "we're not on a branch!"
