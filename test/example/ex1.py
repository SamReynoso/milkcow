from milkcow.test.example.my_model_class import Record
from milkcow import MilkCow


BOB = [Record(**{'name': 'Bob', 'score': 1, 'game': 15})] * 80_000
ALICE = [Record(**{'name': 'Alice', 'score': 1, 'game': 15})] * 80_000

conn = MilkCow(Record)
conn.connect(path='test-mc.db')
conn.push('Bob', BOB)
conn.push('Alice', ALICE)
