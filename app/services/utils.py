class Utils:

    def __init__(self):
        pass

    def log_data(self, message):
        if message is not None:
            print(message)
        else:
            print(f"No data to log")