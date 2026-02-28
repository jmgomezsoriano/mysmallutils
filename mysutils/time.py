import time
try:
    from tqdm.auto import tqdm
except ModuleNotFoundError as e:
    raise ModuleNotFoundError('ModuleNotFoundError: No module named \'tqdm\'. Please install it with the command:\n\n'
                              'pip install tqdm')

def format_shorthand(d: int, h: int, m: int, s: int) -> str:
    """
    Converts time components into a space-separated shorthand string.

    Each non-zero time unit is appended with its corresponding letter
    (d, h, m, s). If a component is zero, it is omitted from the output.

    Args:
        d: Number of days.
        h: Number of hours.
        m: Number of minutes.
        s: Number of seconds.

    Returns:
        A string representing the duration (e.g., '1d 12h 30m').
        Returns an empty string if all inputs are zero.

    Example:
        >>> format_shorthand(1, 0, 45, 10)
        '1d 45m 10s'
    """
    time_format = [f'{t}{unit}' for t, unit in zip([d, h, m, s], ['d', 'h', 'm', 's']) if t]
    return ' '.join(time_format)


def format_timespan(seconds: float, shorthand: bool = False) -> str:
    """
    Converts a total number of seconds into a human-readable duration string.

    Offers two styles:
    1. Digital clock: '01:05', '02:30:10', or '1d 05:00:00'.
    2. Shorthand: '1h 5m' (if letters=True).

    Args:
        seconds: Total seconds to format.
        shorthand: If True, uses abbreviated units (e.g., '1h 5s').
                   If False, uses digital clock format (e.g., '01:00:05').

    Returns:
        The formatted string.
    """
    seconds = int(seconds)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)

    if d > 0:
        return format_shorthand(d, h, m, s) if shorthand else f"{d}d {h:02d}:{m:02d}:{s:02d}"
    if h > 0:
        return format_shorthand(d, h, m, s) if shorthand else f"{h:02d}:{m:02d}:{s:02d}"

    return format_shorthand(d, h, m, s) if shorthand else f"{m:02d}:{s:02d}"


def countdown_timer(seconds: float, description: str = None, leave: bool = False) -> None:
    """
    Pauses execution for a specified duration while displaying a progress bar.

    The bar shows elapsed and remaining time formatted using custom duration logic.

    Args:
        seconds: Total duration of the pause in seconds.
        description: Text prefix to display before the progress bar.
        leave: Whether to keep the progress bar visible after completion.
    """
    if description is None:
        description = f'Waiting {format_timespan(seconds, True)}'
    bar_format = '{l_bar}{bar}| [{elapsed}<{remaining}]'

    with tqdm(total=seconds, desc=description, leave=leave, bar_format=bar_format) as pbar:
        remaining = seconds
        while remaining > 0:
            # Dormimos 1 segundo o el tiempo que falte si es menor a 1
            step = min(1.0, remaining)
            time.sleep(step)
            pbar.update(step)
            remaining -= step
