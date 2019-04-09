def log_info(message):
    #return
    print(f'[INFO] {message}')

def log_warn(message,  error = None):
    #return
    print(f'[WARN] {message}')
    if error is None: return

    print(f'  Error message: {error} \n'
          '  Continue...')

def log_error(message, error = None):
    #return
    print(f'[ERROR] {message}')
    if error is None: return

    print(f'  Error message: {error} \n'
          '  Continue...')

def log_print(*args, **nargs):
    #return
    print(*args, **nargs)
                                                                                                                                                                                                                                                                                                                                                                                                                                