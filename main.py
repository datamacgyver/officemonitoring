from connectors.DatabaseTools import DatabaseTools
from connectors.HiveControls import HiveControls
from connectors.ifttt import action_notification, error_notification
from sensors import limits

hive = HiveControls()


def run_update(variable, db, *args):
    limit = getattr(limits, variable)
    val = limit['func'](*args)
    db.push_new_reading(val, variable)
    db.store_latest_value(variable, val)

    if val > limit['top']:
        respond_to_above(variable, val, db, limit)
    elif val < limit['bottom']:
        respond_to_below(variable, val, db, limit)


def respond_to_above(variable, val, db, limit):
    print("%s above acceptable limit: %s" % (variable, limit['top']))
    action_notification(variable=variable, reading=val)

    if limit['above_action'] is not None:
        hive.run_action_by_name(limit['above_action'])
        db.record_hive_command(limit['above_action'])


def respond_to_below(variable, val, db, limit):
    print("%s below acceptable limit: %s" % (variable, limit['bottom']))
    action_notification(variable=variable, reading=val)

    if limit['below_action'] is not None:
        hive.run_action_by_name(limit['below_action'])
        db.record_hive_command(limit['below_action'])


def main():
    try:
        import sensors.limits
        db = DatabaseTools()
        run_update('stub', db)
        run_update('room_temp', db)
        run_update('cpu_temp', db)
        run_update('room_humidity', db)
    except Exception as E:
        msg = str(E)
        error_notification(msg)
        print('Cataclysmic error occurred. Reported to IFTTT')
        raise
    finally:
        hive.logout()


if __name__ == "__main__":
    main()
