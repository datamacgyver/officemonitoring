from connectors.s3 import push_new_reading, record_hive_command
from connectors.HiveControls import HiveControls
from connectors.ifttt import action_notification, error_notification
from sensors import limits

hive = HiveControls()


def run_update(variable, *args):
    limit = getattr(limits, variable)
    val = limit['func'](*args)
    push_new_reading(val, variable)
    # store_latest_value(variable, val)

    if val > limit['top']:
        respond_to_above(variable, val, limit)
    elif val < limit['bottom']:
        respond_to_below(variable, val, limit)


def respond_to_above(variable, val, limit):
    print("%s above acceptable limit: %s" % (variable, limit['top']))
    action_notification(variable=variable, reading=val)

    if limit['above_action'] is not None:
        hive.run_action_by_name(limit['above_action'])
        record_hive_command(limit['above_action'])


def respond_to_below(variable, val, limit):
    print("%s below acceptable limit: %s" % (variable, limit['bottom']))
    action_notification(variable=variable, reading=val)

    if limit['below_action'] is not None:
        hive.run_action_by_name(limit['below_action'])
        record_hive_command(limit['below_action'])


def main():
    try:
        import sensors.limits
        # run_update('stub', db)
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
