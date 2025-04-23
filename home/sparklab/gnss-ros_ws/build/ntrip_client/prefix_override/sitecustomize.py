import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/sparklab/sparklab/gnss-ros_ws/install/ntrip_client'
