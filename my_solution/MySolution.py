from toypool import ToyPool
from elfpool import ElfPool


# ======================================================================= #
# === MAIN === #

if __name__ == '__main__':

    start = time.time()

    NUM_ELVES = 900
    NUM_TOYS = 100000

    toy_file = os.path.join(os.getcwd(), '..', 'DATA', 'toys_rev2.csv')
    soln_file = os.path.join(os.getcwd(), '..', 'DATA', 'my_solution_num_elves_%d_num_toys_%d.csv' % (NUM_ELVES, NUM_TOYS))

    myelves = create_elves(NUM_ELVES)
    #solution_firstAvailableElf(toy_file, soln_file, myelves)
    solution_firstAvailableIfProductiveElf(toy_file, soln_file, myelves)
    #solution_smallBigQueueElf(toy_file, soln_file, myelves)

    print 'total runtime = {0}'.format(time.time() - start)
