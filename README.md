## Aleo-Monitor

### Requirement
1. Python3 & pip

## Usage
1. Download aleoTool.py to your machine. `wget -O aleoTool.py https://raw.githubusercontent.com/thecodesdev/Aleo-Monitor/main/aleoTool.py`
2. Install tool. `python3 aleoTool.py install`
3. Show help argument to learn. `python3 aleoTool.py -h`
4. Start to use it.

## Commands and Arguments
1. `start` : Activate the robot to monitor your SnarkOS, let the robot do the work. The way the robot works is to see the status of your SnarkOS synchronization, if there is something strange then the robot will warn and restart SnarkOS or do other things if needed to fix it.
2. `status` : To see in detail the status of your SnarkOS. Yup, without the need to type many curl commands from the RPC method available on SnarkOS.
3. `--ip` : The IP address you use to run SnarkOS. If you are using an external IP, please open the port used to run SNarkOS on that IP. Be careful when opening ports. Only available on status argument. Default: 127.0.0.1.
4. `--port` : Port you use to run SnarkOS. Default: 3030.
5. `--attempt` : Number of attempts if you are stuck on one block. If the trial number is reached then this tool will restart or do other things to fix it. Only available on start argument. Default: 0 (disabled).

Note: 1 attempt = 10 seconds.

Sample output:
```Uptime:          4 days, 0:39:43
Block Height:    372975
Block Mined:     46
Duplicate Block: 3363
Role:            Miner
Syncing:         False

Num. Peers:      2 / 736
Connected Peers: 255.255.255.255:4131
                 250.250.250.250:4131

Listening:       0.0.0.0:4131
SnarkOS Version: 1.3.10
```
