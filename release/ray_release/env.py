import os
from typing import Dict

import runfiles
from ray_release.exception import ReleaseTestConfigError

DEFAULT_ENVIRONMENT = "staging_v2"

_REPO_NAME = "com_github_ray_project_ray"


def load_environment(environment_name: str) -> Dict[str, str]:
    file_base = f"{environment_name}.env"
    the_runfiles = runfiles.Create()
    env_file = the_runfiles.Rlocation(
        os.path.join(
            _REPO_NAME,
            "release",
            "ray_release",
            "environments",
            file_base,
        )
    )
    if not os.path.isfile(env_file):
        # No bazel runfiles? Try load based on file local path.
        this_dir = os.path.dirname(__file__)
        env_file = os.path.join(
            this_dir,
            "environments",
        )
        if not os.path.isfile(env_file):
            raise ReleaseTestConfigError(
                f"Unknown environment with name: {environment_name}"
            )

    env = {}
    with open(env_file, "r") as f:
        for line in f.readlines():
            if not line:
                continue
            key, val = line.strip().split("=", maxsplit=1)
            env[key] = val.strip('"')

    return env


def populate_os_env(env: Dict[str, str]) -> None:
    for k, v in env.items():
        os.environ[k] = v
