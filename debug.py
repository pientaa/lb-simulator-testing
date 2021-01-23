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

    print(salp_completed)
    print(random_completed)
    print(sequential_completed)

    salp_allocation = pd.read_csv("./SALP/shard_allocated_6.csv")

    for (node, shards) in salp_allocation.groupby('node'):
        requests_per_node = requests[requests["shard"].isin(shards["shard"].to_list())]

        print("Load:")
        print(requests_per_node['load'].sum())
        print("Num of shards:")
        print(shards.shape[0])


if __name__ == "__main__":
    debug()
