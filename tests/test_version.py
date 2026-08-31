from importlib.metadata import version

from aquasentinel import __version__


def test_runtime_and_package_versions_match():
    assert __version__ == version("aquasentinel-ai")


def test_release_candidate_version():
    assert __version__ == "1.0.0rc1"
