"""Drone artifact directories; development output is grouped by phase."""

from pathlib import Path


def next_phase(root: Path, phase: int) -> tuple[Path, int]:
    """Preserve previous output: repeat invocations go inside phase_N/repeat_M."""
    if isinstance(phase, bool) or not isinstance(phase, int) or phase < 1:
        raise ValueError("phase must be a positive integer")
    target = root / f"phase_{phase}"
    try:
        target.mkdir(parents=True)
        return target, phase
    except FileExistsError:
        if not target.is_dir():
            raise ValueError(f"phase path is not a directory: {target}") from None
    number = 1
    while True:
        repeat = target / f"repeat_{number}"
        try:
            repeat.mkdir()
            return repeat, phase
        except FileExistsError:
            number += 1


def next_run(root: Path) -> tuple[Path, int]:
    """Legacy numbered-run helper; development entry points use next_phase."""
    root.mkdir(parents=True, exist_ok=True)
    number = 1
    while True:
        target = root / f"drone_run_{number}"
        try:
            target.mkdir()
            return target, number
        except FileExistsError:
            number += 1
