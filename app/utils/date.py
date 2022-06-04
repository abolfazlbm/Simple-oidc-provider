from datetime import datetime


def dateid():
    return datetime.now().strftime("%Y%m%d%H%M%S")
