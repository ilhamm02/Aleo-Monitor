import time, os, sys, argparse
from datetime import datetime

args = argparse.ArgumentParser(description='Available Command')
args.add_argument('start', nargs='?', help='run realtime bot monitoring')
args.add_argument('status', nargs='?', help='show snarkos status')
args.add_argument('install', nargs='?', help='install this awesome tool')
args.add_argument('version', nargs='?', help='tool version')
args.add_argument('--port', default='3030', required=False, type=int, help='snarkos rpc port (default: 3030).')
args.add_argument('--ip', default='127.0.0.1', required=False,help='snarkos ip (default: 127.0.0.1) ONLY ON STATUS ARGUMENT.')
args.add_argument('--attempt', default='8', type=int, required=False, help='auto restart when catch up status stuck on same block (default: 20) re-attempt every 10 seconds. ONLY ON START ARGUMENT.')
arg = args.parse_args()

if arg.start == "version":
  print("v0.1.0")
elif arg.start == "install":
  try:
    import requests, colorama
    print("There's nothing to do. You have already installed this tool.")
  except ModuleNotFoundError:
    print("Installing dependencies...")
    os.system('pip install colorama requests > /dev/null 2>&1')
    print("Installed! Now you are ready to use this tool.")
elif arg.start == "start":
  try:
    import requests
    from colorama import Fore, Style
    block = 0
    status = ""
    mined = 0
    sleeping = 1
    attempt = 0
    lastStatus = ""
    endpoint = "http://127.0.0.1:"+str(arg.port)
    blocksPost = """
    {
      "jsonrpc": "2.0", 
      "id":"documentation", 
      "method": "getnodestats", 
      "params": [] 
    }"""
    statusPost = """
    {
      "jsonrpc": "2.0", 
      "id":"documentation", 
      "method": "getnodeinfo", 
      "params": [] 
    }"""

    while True:
      try:
        get = requests.post(endpoint, data=statusPost)
        fullStatus = get.json()
        nowdate = datetime.now()
        now = nowdate.strftime("%H:%M:%S %a %d, %B %Y")
        nowstamp = datetime.timestamp(nowdate)
        status = fullStatus["result"]["is_syncing"]
        get = requests.post(endpoint, data=blocksPost)
        blocks = get.json()
        mined = blocks["result"]["misc"]["blocks_mined"]
        if status == False:
          if blocks["result"]["misc"]["block_height"] > block:
            block = blocks["result"]["misc"]["block_height"]
            print(f"{Fore.GREEN}[SYNCED✓]{Style.RESET_ALL} Latest={block} Mined={mined} {now}")
            sleeping = 1
            attempt = 0
            lastStatus = "synced"
        else:
          if attempt >= arg.attempt:
            os.system('systemctl restart aleod')
            print(f"{Fore.RED}[RESTART]{Style.RESET_ALL} Catching up block {block} too long {now}")
          else:
            if blocks["result"]["misc"]["block_height"] > block:
              block = blocks["result"]["misc"]["block_height"]
              if lastStatus == "catchup":
                sys.stdout.write("\033[F")
              print(f"{Fore.YELLOW}[CATCHUP]{Style.RESET_ALL} Highest={block} Mined={mined} Total Attempt={attempt} {now}")
              sleeping = 1
              attempt = 0
              lastStatus = "catchup"
            elif blocks["result"]["misc"]["block_height"] == block:
              if lastStatus == "catchup":
                sys.stdout.write("\033[F")
              print(f"{Fore.YELLOW}[CATCHUP]{Style.RESET_ALL} Highest={block} Mined={mined} Total Attempt={attempt} {now}")
              block = blocks["result"]["misc"]["block_height"]
              lastStatus = "catchup"
              sleeping = 10
              attempt += 1
        time.sleep(sleeping)
      except KeyboardInterrupt:
        sys.exit(0)
      except argparse.ArgumentError:
        print(f"{Fore.RED}[ ERROR ]{Style.RESET_ALL} Unknown argument")
        sys.exit(0)
      except:
        try:
          nowdate = datetime.now()
          now = nowdate.strftime("%H:%M:%S %a %d, %B %Y")
          if lastStatus == "TRY":
              sys.stdout.write("\033[F")
          print(f"{Fore.YELLOW}[ RETRY ]{Style.RESET_ALL} Trying to get snarkos status {now}")
          lastStatus = "TRY"
          time.sleep(1)
        except KeyboardInterrupt:
          sys.exit(0)
  except ModuleNotFoundError:
    print(f"You must install this awesone tool first. Type: python3 aleoTool.py install")
elif arg.start == "status":
  try:
    import requests
    from colorama import Fore, Style
    try:
      endpoint = "http://"+arg.ip+":"+str(arg.port)
      statusPost = """
      {
        "jsonrpc": "2.0", 
        "id":"documentation", 
        "method": "getnodestats", 
        "params": [] 
      }"""
      infoPost = """
      {
        "jsonrpc": "2.0", 
        "id":"documentation", 
        "method": "getnodeinfo", 
        "params": [] 
      }"""
      peersPost = """
      {
        "jsonrpc": "2.0", 
        "id":"documentation", 
        "method": "getpeerinfo", 
        "params": [] 
      }"""
      get = requests.post(endpoint, data=statusPost)
      stats = get.json()
      get = requests.post(endpoint, data=infoPost)
      info = get.json()
      get = requests.post(endpoint, data=peersPost)
      peer = get.json()
      uptime = info["result"]["launched"]
      uptime = uptime.split('T')
      uptime = uptime[0]+" "+uptime[1]
      uptime = uptime.split('.')
      uptime = uptime[0]
      x = datetime.strptime(uptime, "%Y-%m-%d %H:%M:%S")
      z = datetime.now()
      uptime = str(z-x).split('.')[0]
      block = stats["result"]["misc"]["block_height"]
      mined = stats["result"]["misc"]["blocks_mined"]
      duplicate = stats["result"]["misc"]["duplicate_blocks"]
      mining = info["result"]["is_miner"]
      role = "Non-miner"
      if mining == True:
        role = "Miner"
      status = info["result"]["is_syncing"]
      numPeers = stats["result"]["connections"]["connected_peers"]
      disPeers = stats["result"]["connections"]["disconnected_peers"]
      peers = peer["result"]["peers"]
      listening = info["result"]["listening_addr"]
      version = info["result"]["version"]
      print(f"Uptime: \t {uptime}")
      print(f"Block Height: \t {block}")
      print(f"Block Mined: \t {mined}")
      print(f"Duplicate Block: {duplicate}")
      print(f"Role: \t\t {role}")
      print(f"Syncing: \t {status} \n")
      print(f"Num. Peers: \t {numPeers} / {numPeers+disPeers}")
      print(f"Connected Peers: {peers[0]}")
      for i in peers[1:]:
        print(f"\t\t {i}")
      print(f"\nListening: \t {listening}")
      print(f"SnarkOS Version: {version}")
    except requests.exceptions.ConnectionError:
      print(f"{Fore.RED}[ ERROR ]{Style.RESET_ALL} Failed to get snarkos status")
  except ModuleNotFoundError:
    print(f"You must install this awesone tool first. Type: python3 aleoTool.py install")
