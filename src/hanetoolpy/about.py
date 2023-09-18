try:
    from importlib import metadata
except ImportError:  # for Python<3.8
    import importlib_metadata as metadata

program_name = "hanetoolpy"
build_date = "2023.09.18"

try:
    __version__ = metadata.version("hanetoolpy")
except metadata.PackageNotFoundError:
    __version__ = build_date

version_text = f"version {__version__}"
build_text = f"build {build_date}"
full_version = f"{program_name} | {version_text} ({build_text})"
