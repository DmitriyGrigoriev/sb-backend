# Есть не сортированный список операций:
#from typing import Set, Any
from operator import itemgetter
from itertools import groupby

operations = [
    {"id": 1, "timestamp": 2, "amount": 1},
    {"id": 2, "timestamp": 4, "amount": 8},
    {"id": 1, "timestamp": 3, "amount": 2}
]

# В этом списке операции дублируются по id
# если так случилось, то правильной операцией считается та,
# у которой timestamp более поздний

# Задача: модифицировать функцию filter, так чтобы она
# возвращала только правильные операции
# как только все тесты пройдут - задача решена


def filter(operations: list) -> list:
  rows_by_timestamp = sorted(operations, key=itemgetter('id', 'timestamp'), reverse=True)
  unique_list = []
  for elements, items in groupby(rows_by_timestamp, key=itemgetter('id')):
      for row in items:
          unique_list.append(row)
          break

  print(unique_list)

  return unique_list


def main():
    filter(operations)

if __name__ == '__main__':
    main()
