def log_info(message):
    print(f'[INFO] {message}')

def log_warn(message,  error = None):
    print(f'[WARN] {message}')
    if error is None: return

    print(f'  Error message: {error} \n'
          '  Continue...')



def log_error(message, error = None):
    print(f'[ERROR] {message}')
    if error is None: return

    print(f'  Error message: {error} \n'
          '  Continue...')
