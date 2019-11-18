import numpy as np
import pandas as pd
import threading

from concurrent.futures import ThreadPoolExecutor

FILENAME = 'dataset_diabetes/diabetic_data.csv'
MED_ID = 11
THREADS = 5

"""
Applies a function (func) to a list of (args) using workers threads
"""
def multithreading(func, args, 
                   workers):
    with ThreadPoolExecutor(workers) as ex:
        res = ex.map(func, args)
    return list(res)

"""
Thread Function that creates partially adjacency matrix of medications 
"""
def thread_func(args):
    # note that collecting the args into a tuple is a temporary fix
    start = args[0]
    end = args[1]
    data = args[2]
    num_meds = args[3]
    meds_to_nums = args[4]
    
    adjacency = np.zeros((num_meds, num_meds))
    for ind in range(start, end):
        for ind2 in range(ind + 1, len(data)):
            i = data[ind]
            j = data[ind2]
            if (i[MED_ID] != '?') and (j[MED_ID] != '?') and (i[MED_ID] != j[MED_ID]):
                a = meds_to_nums[i[MED_ID]]
                b = meds_to_nums[j[MED_ID]]
                # similarity in race and gender
                if (i[2] == j[2]) and (i[3] == j[3]):
                    adjacency[a, b] += 1
                    adjacency[b, a] += 1
    print("Task Executed {}".format(threading.current_thread()))
    return adjacency

def main():
    print('reading data from file...')
    data = pd.read_csv(FILENAME).to_numpy()
        
    # create mappings from meds to ids
    print('creating med-id mapping...')
    meds = set()
    for i in data:
        meds.add(i[MED_ID])
    meds.remove('?')
    nums_to_meds = list(meds)
    meds_to_nums = {}
    for ind, m in enumerate(nums_to_meds):
        meds_to_nums[m] = ind
    num_meds = len(nums_to_meds)

    # define arguments for threads by breaking data into sections
    print('defining thread arguments...')
    args = []
    start = 0
    end = int(len(data) / THREADS)
    for i in range(THREADS):
        if i == (THREADS - 1):
            end = len(data)
        args.append((start, end, data, num_meds, meds_to_nums))
        start = end
        end = start + int(len(data) / THREADS)      
    
    # call multithreader
    print('calling multithreader...')
    results = multithreading(thread_func, args, THREADS)
    
    # combine results
    print('combining results of threads')
    adjacency = np.zeros((num_meds, num_meds))
    for result in results:
        adjacency += result

if __name__ == '__main__':
    main()