import csv
from statemachine import State, StateMachine

__all__ = ['HephyDBWriter']

class HephyDBTableWriter(object):

    def __init__(self, writer):
        self.writer = writer

    def __enter__(self):
        return self

    def write(self, **values):
        self.writer.writerow(values)

    def __exit__(self, *args):
        pass

class HephyDBWriter(object):

    class StateMachine(StateMachine):

        init = State('init', initial=True)
        info = State('info')
        tags = State('tags')
        tables = State('tables')

        write_info = init.to(info)
        write_tags = info.to(tags)
        write_table = tags.to(tables) | tables.to.itself()

    def __init__(self, target):
        self.sm = self.StateMachine()
        self.target = target
        self.begin = target.tell()

    def __write_section(self, name):
        if self.target.tell() > self.begin:
            self.target.write(os.linesep)
        writer = csv.writer(self.target)
        writer.writerow(['[{}]'.format(name)])

    def write_info(self, infodict):
        self.sm.write_info()
        self.__write_section('Info')
        writer = csv.DictWriter(self.target, fieldnames=infodict.keys())
        writer.writeheader()
        writer.writerow(infodict)

    def write_tags(self, tags):
        self.sm.write_tags()
        self.__write_section('Tags')
        writer = csv.writer(self.target)
        writer.writerow(tags)

    def write_table(self, name, fieldnames):
        self.sm.write_table()
        self.__write_section(name)
        writer = csv.DictWriter(self.target, fieldnames=fieldnames)
        writer.writeheader()
        return HephyDBTableWriter(writer)
