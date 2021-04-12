#!/usr/bin/env python3
# Standard Library
import inspect
import sys
from subprocess import run


def _inspect_tasks(prefix):
    return {
        f[0].replace(prefix, ""): f[1]
        for f in inspect.getmembers(sys.modules["__main__"], inspect.isfunction)
        if f[0].startswith(prefix)
    }


def _cmd(command, args=[]):
    return run(command.split(" ") + args)


def _exit_handler(status):
    statuses = status if type(status) == list else [status]
    bad_statuses = [s for s in statuses if s.returncode != 0]
    if bad_statuses:
        sys.exit(bad_statuses)


def task_init(args):
    results = []
    results.append(_cmd("python3 -m venv .venv"))
    results.append(_cmd(".venv/bin/python3 -m pip install --upgrade pip setuptools wheel"))
    results.append(_cmd(".venv/bin/python3 -m pip install -r requirements-root.txt"))
    results.append(_cmd(".venv/bin/python3 -m pip list -v --no-index"))
    return results


def task_start(args):
    return _cmd(".venv/bin/python3 -m jupyter lab")


def task_setup_ch(args):
    if len(args) < 1 or int(args[0]) not in range(1, 10):
        raise ValueError("Task 'setup_ch' requires a chapter number. Eg, './task.py setup_ch 3'")

    return _cmd(f".venv/bin/python3 -m pip install -r Ch{args[0]}/requirements.txt")


if __name__ == "__main__":
    tasks = _inspect_tasks("task_")

    if len(sys.argv) >= 2 and sys.argv[1] in tasks.keys():
        _exit_handler(tasks[sys.argv[1]](sys.argv[2:]))
    else:
        print(f"Must provide a task from the following: {list(tasks.keys())}")
