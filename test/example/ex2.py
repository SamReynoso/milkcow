from milkcow.test.example.my_model_class import Record
from milkcow import MilkCow, Receiver
from multiprocessing import Process


receiver = Receiver(Record)
mc = MilkCow(Record)

mc.connect(path='test-mc.db')
mc.pull('Bob')
sender = mc.get_sender()

p = Process(target=sender.send, args=())
p.start()
receiver.recv()

mc.pull('Alice')
sender = mc.get_sender()
p = Process(target=sender.send, args=())
p.start()
receiver.recv()
