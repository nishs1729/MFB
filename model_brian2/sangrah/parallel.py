import numpy as np
import multiprocessing as mp

def par_chunks(func, data, n_chunks=False):
    """
    Parallelize a function by splitting the data into chunks and processing each chunk in a separate process.

    Parameters
    ----------
    func : callable
        The function to be parallelized. It should take a single argument and return a single value.
    data : iterable
        The data to be processed. It should be iterable and can be split into chunks (a list or a numpy array).
    n_chunks : int
        The number of chunks to split the data into. If not specified, the number of chunks is set to the number of cores.

    Returns
    -------
    result : list
        The result of the function applied to each element of data.
    """

    ## set the chunk size to number of cores if not specified
    n_chunks = n_chunks if n_chunks else mp.cpu_count()
    # print(n_chunks)

    ## split the data into chunks
    chunks = np.array_split(data, n_chunks)
    # print(chunks)
    # print(func_chunk(chunks[0]))

    ## parallelize the loop
    with mp.Pool(n_chunks) as p:
        result = p.map(func, chunks)

    return np.concatenate(result)

def chunk_list(lst, n):
    """
    Splits a list into `n` chunks of approximately equal size.

    This function divides the input list into `n` chunks, distributing
    elements as evenly as possible. If the list cannot be divided evenly,
    the remainder elements are distributed one per chunk starting from the
    first chunk.

    Parameters
    ----------
    lst : list
        The list to be split into chunks.
    n : int
        The number of chunks to divide the list into.

    Returns
    -------
    list of lists
        A list containing `n` sublists, each representing a chunk of the
        original list.
    """
    chunk_size = len(lst) // n
    remainder = len(lst) % n
    return [lst[i*chunk_size + min(i, remainder):(i+1)*chunk_size + min(i+1, remainder)] for i in range(n)]


def par_chunks_list(func, data, n_chunks=False):
    """
    Parallelize a function by splitting the data into chunks and processing each chunk in a separate process. 
    This function is similar to `par_chunks` but more robust in that it can handle lists of different lengths.

    Parameters
    ----------
    func : callable
        The function to be parallelized. It should take a single argument and return a single value.
    data : iterable
        The data to be processed. It should be iterable and can be split into chunks (a list or a numpy array).
    n_chunks : int
        The number of chunks to split the data into. If not specified, the number of chunks is set to the number of cores.

    Returns
    -------
    result : list
        The result of the function applied to each element of data.
    """

    ## set the chunk size to number of cores if not specified
    n_chunks = n_chunks if n_chunks else mp.cpu_count()
    # print(n_chunks)

    ## split the data into chunks
    chunks = chunk_list(data, n_chunks)
    # print(chunks)
    # print(func_chunk(chunks[0]))

    ## parallelize the loop
    with mp.Pool(n_chunks) as p:
        result = p.map(func, chunks)

    # return np.concatenate(result)
    return sum(result, [])



if __name__ == '__main__':
    from rich import print
    # example function
    def sqr(x):
        return(x**2)
    
    ## vectorised version of sqr()
    def sqr_vec(x):
        return list(map(sqr, x))

    result = par_chunks(sqr_vec, range(17), 10)
    print(result)

    ##############################################################
    from itertools import product
    import matplotlib.pyplot as plt
    def mandelbrot(c, max_iter=256*16):
        z, i, j = c
        for n in range(max_iter):
            if abs(z) > 2:
                return i, j, n
            z = z*z + c[0]
        return i, j, max_iter
    

    def mandelbrot_vec(c, max_iter=256):
        return list(map(mandelbrot, c))
    
    width = 100
    height = 100

    data = []
    for i,j in product(range(height), range(width)):
        c = complex(j/width*3.5 - 2.5, i/height*2 - 1)
        data.append([c, i, j])
    # print(data)

    res = par_chunks_list(mandelbrot_vec, data, 40)
    result = np.zeros((height, width))
    for i, j, n in res:
        result[i, j] = n
    print(result)

    plt.imshow(result)
    plt.show()

    ##############################################################
