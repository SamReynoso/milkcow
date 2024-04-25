from milkcow.test.example.my_model_class import Record
from milkcow import MilkCow, Receiver
from multiprocessing import Process


def ex1():
    print('I am 1')
    BOB = [Record(**{'name': 'Bob', 'score': 1, 'game': 15})] * 80_000
    ALICE = [Record(**{'name': 'Alice', 'score': 1, 'game': 15})] * 80_000

    mc = MilkCow(Record)
    mc.connect(path='test-mc.db')
    print(mc)
    mc.push('Bob', BOB)
    print(mc)
    mc.push('Alice', ALICE)
    print(mc)


def ex2():
    print('I am 2')
    mc = MilkCow(Record)
    mc.connect(path='test-mc.db')

    mc.pull('Bob')
    sender = mc.sender.keyed_sender('Alice')
    receiver = Receiver(Record)
    p = Process(target=sender.send, args=())
    p.start()
    receiver.recv_model()
    print(receiver)

    mc.pull('Alice')
    sender = mc.sender.new_sender()
    p = Process(target=sender.send, args=())
    p.start()
    receiver.recv_model()
    print(receiver)
