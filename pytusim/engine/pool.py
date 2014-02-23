from multiprocessing.pool   import ThreadPool as Pool

def getPool():
    return Pool( processes=5 )
