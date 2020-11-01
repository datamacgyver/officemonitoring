from datetime import datetime


def _get_time_diff(var):
    """Get the difference between the last run time for a variable and now"""
    with open(var+'.timer', 'r') as f:
        time = f.read()
    time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
    now = datetime.now()
    diff = now-time
    return diff.seconds / 60


def needs_to_run(var, min_diff):
    """
    Determine if a given variable needs to run.

    Parameters
    ----------
    var : str
        Name of variable. Used for logging time and checking previous times.
    min_diff : int
        What's the minimum difference (in minutes) needed before we rerun?

    Returns
    -------
    bool
        Do we need to run the given variable.

    """
    try:
        diff = _get_time_diff(var)
    except FileNotFoundError:
        return True

    if int(diff) > min_diff:
        return True
    else:
        return False


def note_this_run(var):
    """Record that a variable has just been run"""
    now = datetime.now()
    with open(var+'.timer', 'w') as f:
        return f.write(str(now))


if __name__ == '__main__':
    print(needs_to_run('test', 1))
    # print(note_this_run('test'))
    # print(needs_to_run('test', 1))
    # print(_get_time_diff('test'))