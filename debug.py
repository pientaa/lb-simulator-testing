import pandas as pd


def debug():
    load_vectors_df = pd.read_csv("load_vectors.csv", header=None)
    requests = pd.read_csv("requests.csv")

    salp_completed = pd.read_csv("./SALP/requests_completed_6.csv")
    random_completed = pd.read_csv("./random/requests_completed_6.csv")
    sequential_completed = pd.read_csv("./sequential/requests_completed_6.csv")

    print(salp_completed['delay'].sum())
    print(random_completed['delay'].sum())
    print(sequential_completed['delay'].sum())

    print(requests['load'].sum())

    print(salp_completed)
    print(random_completed)
    print(sequential_completed)

    salp_allocation = pd.read_csv("./SALP/shard_allocated_6.csv")
    random_allocation = pd.read_csv("./random/shard_allocated_6.csv")
    sequential_allocation = pd.read_csv("./sequential/shard_allocated_6.csv")

    shard_load_df = load_vectors_df.sum(axis=1)
    shard_load = pd.DataFrame(shard_load_df, columns=['load'])
    shard_load['shard'] = range(1, 601)

    print("Total cloud load: ", round(shard_load_df.sum(), 2))

    check_generator(shard_load, requests)

    print_allocation_load(salp_allocation, requests, "SALP", shard_load)
    print_allocation_load(random_allocation, requests, "random", shard_load)
    print_allocation_load(sequential_allocation, requests, "sequential", shard_load)


def check_generator(shard_load, requests):
    for (shard, grouped_requests) in requests.groupby('shard'):
        foo = shard_load[shard_load['shard'] == shard]['load'].sum()
        print("Shard: " + str(shard) + " load: " + str(grouped_requests['load'].sum()) + ", another method load: " + str(foo * 5.0))


def print_allocation_load(allocation_df, requests, algorithm, shard_load):
    print("-------------------------------------")
    print("--------------  " + algorithm + "  --------------")
    print("Number of shards: ", str(allocation_df.groupby("node").count().sum().item()))

    total_allocated_load = 0
    for (node, shards) in allocation_df.groupby('node'):
        shards_list = shards['shard'].tolist()
        load_per_node = shard_load.loc[shard_load["shard"].isin(shards_list)]
        node_load = load_per_node['load'].sum()
        print("Node: ", str(node), " load: ", str(round(node_load, 2)))
        total_allocated_load += node_load

    print("Sum total allocated load: ", str(round(total_allocated_load, 2)))

    print("----------------ANOTHER METHOD------------------")

    for (node, shards) in allocation_df.groupby('node'):
        requests_per_node = requests[requests["shard"].isin(shards["shard"].to_list())]

        print("Node: ", str(node), " load: ", str(round(requests_per_node['load'].sum()/5.0, 2)))
        print("Num of shards: " + str(shards.shape[0]))


if __name__ == "__main__":
    debug()
