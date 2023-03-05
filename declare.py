import argparse
import inspect

__all__ = ["main"]

parser = argparse.ArgumentParser()
subcmds = parser.add_subparsers(required=True, dest="_subcmd")

subcmd_to_function = {}


def run_chosen_subcommand():
    args = parser.parse_args()
    func = subcmd_to_function[args._subcmd]
    sig = inspect.signature(func)
    pos, kw = [], {}
    for param in sig.parameters.values():
        if not hasattr(args, param.name):
            continue
        match param.kind:
            case inspect.Parameter.POSITIONAL_ONLY:
                pos.append(getattr(args, param.name))
            case inspect.Parameter.KEYWORD_ONLY:
                kw[param.name] = getattr(args, param.name)
            case _:
                assert False, f"parameter kind not implemented: {param.kind}"
    return func(*pos, **kw)


def add_subcommand(func):
    p = subcmds.add_parser(func.__name__, description=func.__doc__)
    subcmd_to_function[func.__name__] = func
    sig = inspect.signature(func)
    for param in sig.parameters.values():
        kw = {}

        if param.annotation != inspect.Parameter.empty:
            kw["type"] = param.annotation

        if param.default == inspect.Parameter.empty:
            kw["required"], kw["default"] = True, None
        else:
            kw["required"], kw["default"] = False, param.default

        match param.kind:
            case inspect.Parameter.POSITIONAL_ONLY:
                names = [param.name]
                if not kw["required"]:
                    kw["nargs"] = "?"
                del kw["required"]
            case inspect.Parameter.KEYWORD_ONLY:
                names = [f"--{param.name}"]
            case _:
                assert False, f"parameter kind not implemented: {param.kind}"

        p.add_argument(*names, **kw)


def main(func=None):
    return add_subcommand(func) if func is not None else run_chosen_subcommand()
