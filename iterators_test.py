class MyIterator:

    def __init__(self, list_):
        self.list_ = list_
        self.cur = -1
        self.nest_cur = 0
        self.list_len = len(self.list_)

    def __iter__(self):
        self.cur += 1
        self.nest_cur = 0
        return self

    def __next__(self):
        while (self.cur - self.list_len) and (self.nest_cur == len(self.list_[self.cur])):
            iter(self)
        if self.cur == self.list_len:
            raise StopIteration
        self.nest_cur += 1
        return self.list_[self.cur][self.nest_cur - 1]


if __name__ == '__main__':

    nested_list = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None],
    ]

    for item in MyIterator(nested_list):
        print(item)

    flat_list = [item for item in MyIterator(nested_list)]
    print(flat_list)