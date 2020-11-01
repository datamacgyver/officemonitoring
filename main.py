from connectors.s3 import push_new_reading, record_hive_command
from connectors.HiveControls import HiveControls
from connectors.ifttt import action_notification, error_notification
from sensors.timing_checks import needs_to_run, note_this_run
from sensors import sensor_config

hive = HiveControls()


def run_update(variable_name, *args):
    """Run an update for an office variable and decide what to do with the result"""

    variable_setting = getattr(sensor_config, variable_name)

    # Do we need to run variable?
    if not needs_to_run(variable_name, variable_setting['minutes_to_wait']):
        print('Insufficient time since last check! Aborting %s' % variable_name)
        return
    else:
        note_this_run(variable_name)
        print('Running %s' % variable_name)

    # Make observation
    val = variable_setting['func'](*args)

    # Do we need to record the output?
    update_rule = variable_setting['record_outcome'].lower()
    if update_rule == 'always':
        push_new_reading(val, variable_name)
    elif update_rule == 'if true' and val:
        push_new_reading(val, variable_name)
    elif update_rule == 'if false' and not val:
        push_new_reading(val, variable_name)

    # What do we need to do given the output?
    if val >= variable_setting['upper']:
        _run_action(variable_name, val, variable_setting, 'above')
    elif val < variable_setting['lower']:
        _run_action(variable_name, val, variable_setting, 'below')
    
    print("Finished %s" % variable_name)


def _run_action(variable, val, limit, typ):
    """Given an action is stipulated in the update, what should be done?"""
    if typ == 'below':
        limit_val = limit['lower']
        action = limit['below_action']
    elif typ == 'above':
        limit_val = limit['upper']
        action = limit['above_action']
    else:
        raise ValueError("typ must be above or below, not %s" % typ)

    if action is not None:
        print("%s %s acceptable limit: %s" % (variable, action, limit_val))
        action_notification(variable=variable, reading=val)
        hive.run_action_by_name(action)
        record_hive_command(action)


def main():
    try:
        import sensors.sensor_config
        # run_update('stub', db)
        run_update('room_motion')
        run_update('room_temp')
        run_update('cpu_temp')
        run_update('room_humidity')
    except Exception as E:
        msg = str(E)
        error_notification(msg)
        print('Cataclysmic error occurred. Reported to IFTTT')
        raise
    finally:
        hive.logout()


if __name__ == "__main__":
    main()
