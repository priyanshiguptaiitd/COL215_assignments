from time import time

def time_it(func): 
    """ time_it - Wrapper for timing function exectution

    Args:
        func (_type_): The function we want to pass to our timing wrapper
    """
    def wrap_func_timeit(*args, **kwargs): 
        t_start = time() 
        result = func(*args) 
        t_end = time()
        if(not kwargs["supress_time_out"]): 
            print(f'Function {func.__name__!r} executed in {(t_end-t_start):.4f}s and produced output : {result[2]}') 
        return result,(t_end-t_start) 
    return wrap_func_timeit

