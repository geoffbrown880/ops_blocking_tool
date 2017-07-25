#! /c/Python34/python
#
# Written by Geoff Brown
# It's not completely bullshit...
# Zach helped too with the scheduling algorithm
#
#      OOOOOOOOO     PPPPPPPPPPPPPPPPP
#    OO:::::::::OO   P::::::::::::::::P
#  OO:::::::::::::OO P::::::PPPPPP:::::P
# O:::::::OOO:::::::OPP:::::P     P:::::P
# O::::::O   O::::::O  P::::P     P:::::P   ssssssssss
# O:::::O     O:::::O  P::::P     P:::::P ss::::::::::s
# O:::::O     O:::::O  P::::PPPPPP:::::Pss:::::::::::::s
# O:::::O     O:::::O  P:::::::::::::PP s::::::ssss:::::s
# O:::::O     O:::::O  P::::PPPPPPPPP    s:::::s  ssssss
# O:::::O     O:::::O  P::::P              s::::::s
# O:::::O     O:::::O  P::::P                 s::::::s
# O::::::O   O::::::O  P::::P           ssssss   s:::::s
# O:::::::OOO:::::::OPP::::::PP         s:::::ssss::::::s
#  OO:::::::::::::OO P::::::::P         s::::::::::::::s
#    OO:::::::::OO   P::::::::P          s:::::::::::ss
#      OOOOOOOOO     PPPPPPPPPP           sssssssssss


from lib.tool_classes import *

r = Roster('roster.csv')

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
stat = ['Truck', 'Polaris', 'RP', 'Waldron', 'Russell 1', 'Russell 2', 'Intra 1', 'Intra 2', 'Shreve/Elliott', 'MacArthur/University']

s = Schedule(days, stat, r)
s.gen_schedule(threshold=3)
s.write_to_file('schedule.csv')

print([s.misses] + days)
for lines in s.flatten():
    print(lines)


