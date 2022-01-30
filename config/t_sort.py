# Есть не сортированный список операций:
from typing import Set, Any, List
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
  for _, items in groupby(rows_by_timestamp, key=itemgetter('id')):
      for row in items:
          unique_list.append(row)
          break

  print(unique_list)

  return unique_list


class Solution:
    @classmethod
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        hashmap = {}
        for i in range(len(nums)):
            hashmap[nums[i]] = i
        for i in range(len(nums)):
            complement = target - nums[i]
            if complement in hashmap and hashmap[complement] != i:
                return [i, hashmap[complement]]

def main():
    # filter(operations)
    Solution().twoSum(nums = [2,7,11,15], target = 9)


if __name__ == '__main__':
    main()
