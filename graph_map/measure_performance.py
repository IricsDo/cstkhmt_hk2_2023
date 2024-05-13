import time
import random
import datetime
import tracemalloc
import shortest_path as spath
from matplotlib import pyplot as plt

if __name__ == '__main__':

    slo = None
    with spath.aloader.Loader("Loading alogrithm...", "Algorithm already!"):
        slo = spath.I_Graph()
        slo.load_graph('graph_map/data/Road/Co_Giang_Road.geojson')
        slo.load_algorithm()
    slo.info_graph()

    print('\n\n')
    # Run 3 alogrithm parallel and measure the time, only one shortest-path, no visualize
    '''
    start_vertex = str(random.randint(0, slo.get_nodes() - 1))
    end_vertex = str(random.randint(0, slo.get_nodes() - 1))
    start_time = time.time()
    print(f"\n===>>> Calculating shortest-path between {start_vertex} and {end_vertex} <<<===")
    print('Please wating ...')
    # slo.run_parallel(start_vertex, end_vertex, False)
    executed_time = round(time.time() - start_time)
    print("\n\nTime executed: {}".format(str(datetime.timedelta(seconds=executed_time))))
    '''

    # Run 3 alogrithm sequence and measure the time
    # For one shortest path and k-shortest path 

    texecuted = dict()
    mtexecuted = dict()

    algorithm_name = ['dijkstra', 'bellman_ford', 'floyd_warshall']
    count = 1
    while count < 100:
        print(f'#{count}')
        start_vertex = str(random.randint(0, slo.get_nodes() - 1))
        end_vertex = str(random.randint(0, slo.get_nodes() - 1))
        success = False
        for algo in algorithm_name:
            print(f'###################### algo = {algo} ######################')
            if algo not in texecuted:
                texecuted[algo] = []
                mtexecuted[algo] = []

            start_time = time.time()
            tracemalloc.start()
            
            result = slo.run_sequence(algo, start_vertex, end_vertex, False, False)
            # result = slo.run_sequence(algo, start_vertex, end_vertex, True, False)

            size, peak = tracemalloc.get_traced_memory()
            tracemalloc.reset_peak()

            if tracemalloc.is_tracing():
                tracemalloc.clear_traces()
                tracemalloc.stop()

            if result == None or len(result) == 0:
                print(f"Faild in this case ({start_vertex}, {end_vertex})")
                print("Bypass all algorithm, try next time !")
                success = False
                break
            executed_time = round(time.time() - start_time, 3)
            executed_mem = round((peak - size)/1024, 3)
            print("Time executed: {}".format(str(datetime.timedelta(seconds=round(executed_time)))))
            texecuted[algo].append(executed_time)
            mtexecuted[algo].append(executed_mem)
            success = True
        print('\n')

        if success:
            count += 1
    
    indexs = [i for i in range(1, count)]
    figure, axis = plt.subplots(1, 2) 
    figure.suptitle("Measure Performance For One Path", fontweight ="bold")
    figure.tight_layout()

    axis[0].plot(indexs, texecuted['dijkstra'], color='#FF0000', linestyle='--', marker='.')
    axis[0].plot(indexs, texecuted['bellman_ford'], color='#000BFF', linestyle='dashdot' ,marker='x')
    axis[0].plot(indexs, texecuted['floyd_warshall'], color='#B40062', linestyle='dotted', marker='o')
    axis[0].set_title('Time Measure')
    axis[0].set_ylabel('Time executed (s)')
    axis[0].set_xlabel('Number of test (n)')
    axis[0].legend(algorithm_name)
    axis[0].grid(True)

    axis[1].plot(indexs, mtexecuted['dijkstra'], color='#FF0000', linestyle='--', marker='.')
    axis[1].plot(indexs, mtexecuted['bellman_ford'], color='#000BFF', linestyle='dashdot' ,marker='x')
    axis[1].plot(indexs, mtexecuted['floyd_warshall'], color='#B40062', linestyle='dotted', marker='o')
    axis[1].set_title('Memory Measure')
    axis[1].set_ylabel('Memory executed (KiB)')
    axis[1].set_xlabel('Number of test (n)')
    axis[1].legend(algorithm_name)
    axis[1].grid(True)

    plt.savefig("graph_map/one_shortest_measure.jpg")

    print('Done')
    print('\n')
    exit(0)