from milkcow import ObjectCow
from milkcow.test.example import Record


def ex4():
    print('I am 4')
    oc = ObjectCow(Record)
    oc.connect('test-mc.db')
    oc.pull('Bob')

    print(oc)
    objs = oc.new('Bob')

    oc.push('Bob', objs)

    objs = oc.new('Bob')

    print(oc)
    print(len(objs))






