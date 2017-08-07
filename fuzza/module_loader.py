"""
fuzza.module_loader
-------------------

This module is used as a helper to dynamically load modules.
"""
import importlib.util


def load_module(name, namespace_prefix, default_name):
    """
    Load module given the module name. The loader has a decision logic
    that falls through as follows,

        1. Load the default module if ``name`` is ``None``.
        2. Load built-in module based on concatenation of prefix and
            user-specified module name.
        3. Load module based on the name.

    Args:
        name (str): The name of module to load.
        namespace_prefix (str): The prefix of module namespace to be
            concatenated.
        default_name (str): The name of default module to load.

    Returns:
        The loaded module.

    Raises:
        ModuleNotFoundError: If module spec cannot be found after all
            attempts.
    """
    spec = None

    if name is None:
        spec = importlib.util.find_spec(default_name)
    else:

        spec = importlib.util.find_spec(namespace_prefix + name)

        if spec is None:
            spec = importlib.util.find_spec(name)

    if spec is None:
        raise ModuleNotFoundError("No module named '%s'" % name)

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module
