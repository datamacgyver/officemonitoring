from connectors.s3 import push_new_reading, record_hive_command
from connectors.HiveControls import HiveControls
from connectors.ifttt import action_notification, error_notification
from sensors import variable_settings

hive = HiveControls()


def run_update(variable_name, *args):
    variable_setting = getattr(variable_settings, variable_name)
    val = variable_setting['func'](*args)
    push_new_reading(val, variable_name)
    # store_latest_value(variable_name, val)

    if val > variable_setting['upper']:
        respond_to_above(variable_name, val, variable_setting)
    elif val < variable_setting['lower']:
        respond_to_below(variable_name, val, variable_setting)


def respond_to_above(variable, val, limit):
    print("%s above acceptable limit: %s" % (variable, limit['upper']))
    action_notification(variable=variable, reading=val)

    if limit['above_action'] is not None:
        hive.run_action_by_name(limit['above_action'])
        record_hive_command(limit['above_action'])


def respond_to_below(variable, val, limit):
    print("%s below acceptable limit: %s" % (variable, limit['lower']))
    action_notification(variable=variable, reading=val)

    if limit['below_action'] is not None:
        hive.run_action_by_name(limit['below_action'])
        record_hive_command(limit['below_action'])


def main():
    try:
        import sensors.variable_settings
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
