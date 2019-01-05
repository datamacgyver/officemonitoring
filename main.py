from connectors.DatabaseTools import DatabaseTools
from connectors.HiveControls import HiveControls
from connectors.ifttt import action_notification, error_notification
from sensors import limits

# TODO: What do None's do in monitor loop? Should make it raise?
# TODO: Proper excepts in DB tools. try/catches for failed pushes. What to do?
# TODO: push to a table that contains only the most recent of each variable
# TODO: Add example secure files to secure folder.
# TODO: logoff in class delete not working in Hive Controls

hive = HiveControls()


def run_update(variable, db, *args):
    limit = getattr(limits, variable)
    val = limit['func'](*args)
    db.push_value(val, variable)
    if val > limit['top']:
        print("%s above acceptable limit: %s" % (variable, limit['top']))
        action_notification(variable=variable, reading=val)
        hive.run_action(limit['above_action'])
    elif val < limit['bottom']:
        print("%s below acceptable limit: %s" % (variable, limit['bottom']))
        action_notification(variable=variable, reading=val)
        hive.run_action(limit['above_action'])


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
