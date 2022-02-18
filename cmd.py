# Some system might have to run this command with sudo.
# sysctl -w net.core.rmem_max=2500000
# Please visit the following website to read more about the issue.
# https://github.com/lucas-clemente/quic-go/wiki/UDP-Receive-Buffer-Size

import subprocess

def cmd(arg):
    x = subprocess.run(arg, stdout=subprocess.PIPE, shell=True)
    return x

if __name__=="__main__":
    print(cmd("ipfs version").stdout.decode())