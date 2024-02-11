tileIndex = "white"
def get_index_rank(index):
    return (index // 8) + 1


def get_index_file(index):
    return (index % 8) + 1


def get_index(rank, file):
    return (rank * 8) + file
