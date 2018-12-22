import monitors as m
from DatabaseTools import DatabaseTools

db = DatabaseTools()

while True:
    test_val = m.get_stub_value()
    db.push_value([test_val], 'cpu_temp', ['cpu_temp'])
    break
    



