from datetime import datetime

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

server_start = get_timestamp()

def get_server_info():
    return {
        "server_start": server_start,
        "current_time": get_timestamp(),

}
