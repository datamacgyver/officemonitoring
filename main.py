import urllib.parse as p

from connectors.DatabaseTools import DatabaseTools
from connectors.HiveControls import HiveControls
from connectors.ifttt import send_request
from sensors import limits

# TODO: push to a table that contains only the most recent of each variable
# TODO: Add example secure files to secure folder.

hive = HiveControls()


def run_update(variable, db, *args):
    limit = getattr(limits, variable)
    val = limit['func'](*args)
    db.push_value(val, variable)
    if val > limit['top']:
        send_request(variable + '_above_max')
        hive.run_action(limit['above_action'])
    elif val < limit['bottom']:
        send_request(variable + '_below_min')
        hive.run_action(limit['above_action'])


def main():
    try:
        import sensors.limits
        db = DatabaseTools()
        run_update('stub', db)
        run_update('cpu_temp', db)
        run_update('room_temp', db)
        run_update('room_humidity', db)
    except Exception as E:
        msg = p.quote_plus(str(E))
        send_request('cataclysm_occurred', json={'Value1': msg})
        print('Cataclysmic error occurred. Reported to IFTTT')
        raise
    finally:
        hive.logout()


if __name__ == "__main__":
    main()
