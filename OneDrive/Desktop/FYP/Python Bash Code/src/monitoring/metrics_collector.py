import psutil

def collect_metrics():
    """
    Collect system metrics using psutil.
    Returns a dictionary with CPU, memory, and disk usage percentages.
    """
    # CPU usage percentage over an interval of 1 second
    cpu_usage = psutil.cpu_percent(interval=1)
    
    # Memory usage percentage (used memory / total memory * 100)
    memory_usage = psutil.virtual_memory().percent
    
    # Disk usage percentage for the root partition
    disk_usage = psutil.disk_usage('/').percent
    
    return {
        'cpu_usage_percent': cpu_usage,
        'memory_usage_percent': memory_usage,
        'disk_usage_percent': disk_usage
    }
 
def get_network_metrics():
    """
    Return aggregate network I/O counters.
    """
    io = psutil.net_io_counters()  # system-wide totals
    return {
        'net_bytes_sent': io.bytes_sent,       # total bytes sent
        'net_bytes_recv': io.bytes_recv,       # total bytes received
        'net_packets_sent': io.packets_sent,   # total packets sent
        'net_packets_recv': io.packets_recv,   # total packets received
        'net_errin': io.errin,                 # total incoming errors
        'net_errout': io.errout,               # total outgoing errors
        'net_dropin': io.dropin,               # total incoming dropped packets
        'net_dropout': io.dropout              # total outgoing dropped packets
    }
