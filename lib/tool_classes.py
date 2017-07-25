# classes, classes, and more classes

from csv import reader, writer, excel
from random import choice
from itertools import product


class Blocker:
    def __init__(self, name, schedule, training, one, ten):

        # type-checking
        if not all([
            type(name) is str,
            type(schedule) is list,
            type(training) is list
        ]):
            raise TypeError('Param <name> must be str; <schedule> '
                            'and <training> must be list.')

        self.name = name
        self.first, self.last = tuple(self.name.split(' '))
        self.days_blocked = {
            'Monday': False,
            'Tuesday': False,
            'Wednesday': False,
            'Thursday': False,
            'Friday': False,
        }
        self.one = one
        self.ten = ten
        self.schedule = {
            'Monday': schedule[0],
            'Tuesday': schedule[1],
            'Wednesday': schedule[2],
            'Thursday': schedule[3],
            'Friday': schedule[4],
        }
        self.training = {
            'Polaris': training[1],
            'Gator': training[2],
            'Truck': training[2],
            'RP': training[0]
        }

    def __repr__(self):
        return 'Blocker: {}'.format(self.name)

    def train(self, pos, tf):
        if pos not in [
            'Polaris', 'Gator', 'Truck', 'RP'
        ]:
            raise ValueError('Not a valid position!')

        self.training[pos] = tf

    def update_schedule(self, pos, tf):
        if pos not in ['Monday',
                       'Tuesday',
                       'Wednesday',
                       'Thursday',
                       'Friday']:
            raise ValueError('Not a valid date/position!')

        self.schedule[pos] = tf

    def block(self, day):
        self.days_blocked[day] = True

    def check(self, day, pos, threshold, desperate=False):

        times_blocked = 0
        for int_day in self.days_blocked:
            if self.days_blocked[int_day]:
                times_blocked += 1

        # don't pick 1s
        if not desperate and self.one:
            return False

        # don't pick 10s more than once
        if not desperate and self.ten and times_blocked >= 1:
            return False

        # don't pick those who aren't trained
        if pos in self.training:
            if not all([self.schedule[day], self.training[pos]]):
                return False

        # don't pick people twice on the same day
        if self.days_blocked[day]:
            return False

        # don't pick people more than X times a week
        if not desperate and times_blocked >= threshold:
            return False

        # don't pick those who can't block!
        if not self.schedule[day]:
            return False

        return True


class Schedule:
    def __init__(self, days, stations, roster):

        # type-checking
        if not all([type(l) is list for l in (days, stations)]):
            raise TypeError("Args must be lists.")

        self.days = days
        self.stations = stations
        self.roster = roster
        self.misses = 0

        self.schedule = {
            day: {
                pos: ['' * len(self.days)] for pos in self.stations
            }
            for day in self.days
        }

        # for swimming in
        self.pools = []

        # blockers are put in via a roster
        self.blockers = self.roster.blockers
        if not all([type(b) is Blocker for b in self.blockers]):
            raise TypeError("All members must be type <Blocker>!")

    # generate the pool based on the position being filled
    def gen_pools(self, combos, threshold, desperate=False):
        self.pools = []

        for tup in combos:
            int_pool = []

            for b in self.blockers:
                if b.check(tup[0], tup[1], threshold, desperate):
                    int_pool += [b]

            tup += (int_pool,)
            self.pools += [tup]

        # a slightly hairy statement to sort by the availability per day
        self.pools = sorted(self.pools, key=lambda pool_tup: len(pool_tup[2]))

    # generate a schedule!
    def gen_schedule(self, threshold=2):

        self.misses = 0

        # a list of all the combinations that we have
        combos = list(product(self.days, self.stations))

        # we can't do a for-each here...
        for i in range(len(combos)):
            self.gen_pools(combos, threshold)

            day, pos, pool = self.pools[0]
            b = choice(pool) if pool else None

            if b:
                b.block(day)
                self.schedule[day][pos] = b.name

            else:
                self.schedule[day][pos] = ''
                self.misses += 1

            combos.remove((day, pos))

    def write_to_file(self, filename):
        with open(filename, 'w') as csvfile:
            write = writer(csvfile, dialect=excel, lineterminator='\n')
            write.writerow([''] + self.days)

            rows = self.flatten()
            for row in rows:
                write.writerow(row)

    def flatten(self):
        arr = []

        for pos in self.stations:
            int_arr = [pos]
            for day in self.days:
                int_arr += [self.schedule[day][pos]]

            arr += [int_arr]

        return arr


class Roster:
    def __init__(self, inp=None):
        self.blockers = []
        if type(inp) is list:
            self.blockers = inp
        elif type(inp) is str:
            self.gen_from_file(inp)
        else:
            raise TypeError("This constructor takes only lists or strings!")

    # add a blocker to the roster
    def add(self, blocker):
        if type(blocker) is not Blocker:
            raise TypeError("You can only add blockers!")

        self.blockers += [blocker]

    # remove a blocker at a certain index
    def remove(self, index):
        self.blockers.remove(index)

    # generates a roster object from the csv
    def gen_from_file(self, filename):
        with open(filename, 'r') as csvfile:

            # skip the first line...
            csvfile.__next__()
            read = reader(csvfile, dialect=excel)

            # generate some blockers
            for row in read:
                name = row[0]
                sched = [False if x else True for x in row[1:6]]
                one = True if row[6] else False
                ten = True if row[7] else False
                train = [True if x else False for x in row[8:11]]

                b = Blocker(name, sched, train, one, ten)
                self.blockers += [b]

    def write_to_file(self, filename):
        with open(filename, 'w') as csvfile:
            write = writer(csvfile, dialect=excel, lineterminator='\n')
            write.writerow(['Name', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                            'RL', '10', 'RP', 'Polaris', 'Truck'])

            rows = self.flatten()
            for row in rows:
                write.writerow(row)

    # make an array of arrays for writing to a file
    def flatten(self):
        arr = []

        # order by first name
        for b in sorted(self.blockers, key=lambda blocker: blocker.name):
            b_arr = [b.name]
            for day in ['Monday',
                        'Tuesday',
                        'Wednesday',
                        'Thursday',
                        'Friday']:
                b_arr += [''] if b.schedule[day] else ['X']

            b_arr += ['X'] if b.one else ['']
            b_arr += ['X'] if b.ten else ['']

            for pos in ['RP', 'Polaris', 'Truck']:
                b_arr += ['X'] if b.training[pos] else ['']

            arr += [b_arr]

        return arr

    # get the day order based on least to most
    def get_day_order(self, sched_days):
        int_days = {day: 0 for day in sched_days}

        for b in self.blockers:
            for day in sched_days:
                if b.schedule[day]:
                    int_days[day] += 1

        return sorted(int_days, key=int_days.get)
