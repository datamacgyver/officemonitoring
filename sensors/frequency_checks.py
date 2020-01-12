from datetime import datetime


def _get_time_diff(var):
    with open(var+'.timer', 'r') as f:
        time = f.read()
    time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
    now = datetime.now()
    return (now - time).min


def needs_to_run(var, min_diff):

    try:
        diff = _get_time_diff(var)
    except FileNotFoundError:
        return True

    if int(diff) > min_diff:
        return True
    else:
        return False


def note_this_run(var):
    now = datetime.now()
    with open(var+'.timer', 'w') as f:
        return f.write(str(now))
