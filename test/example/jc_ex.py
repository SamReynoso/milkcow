from milkcow import JqCow
from milkcow import milkcat


def ex3():
    print('I am 3')
    jc = JqCow('name')
    print(jc)

    jc.connect('test-mc.db')
    jc.pull('Bob')
    values = jc.new('Bob')[:5]
    for val in values[:5]:
        print(val)
        pass
    print()

    print(jc)
    raw_json = milkcat.dump(values)
    jc.push_raw_json(raw_json)
    print(jc)












