import asyncio
import json
import websockets
import requests
from colorama import Fore, Style
from random import randint
from time import sleep

def split_chunk(var):
    if isinstance(var, int):
        var = str(var)
    n = 3
    var = var[::-1]
    return ' '.join([var[i:i + n] for i in range(0, len(var), n)])[::-1]

class Battle:
    wins = 0
    loses = 0

    def __init__(self):
        with open('config.json', 'r') as file:
            config = json.load(file)
        
        self.secret = config['secret']
        self.tgId = config['tgId']
        self.initData = config['initData']
        self.telegram_bot_token = config['telegram_bot_token']
        self.telegram_chat_id = config['telegram_chat_id']
        self.websocket: websockets.WebSocketClientProtocol = None
        self.battleId = ""
        self.superHit = False
        self.strike = {
            "defense": False,
            "attack": False
        }
        self.stop_event = asyncio.Event()

    def send_telegram_notification(self, message):
        url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
        payload = {
            "chat_id": self.telegram_chat_id,
            "text": message
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"🍓 {Fore.RED+Style.BRIGHT}[ Error Telegram ]\t: {e}")

    async def sendHit(self):
        while not self.stop_event.is_set():
            if self.superHit:
                await asyncio.sleep(0.4)
                continue
            
            content = [
                "HIT",
                {
                    "battleId": self.battleId
                }
            ]
            try:
                await self.websocket.send(f"42{json.dumps(content)}")
            except:
                return
            await asyncio.sleep(0.11)

    async def listenerMsg(self):
        while not self.stop_event.is_set():
            try:
                data = await self.websocket.recv()
            except Exception as err:
                self.stop_event.set()
                return

            if data.startswith('42'):
                data = json.loads(data[2:])
                
                if data[0] == "HIT":
                    print(f"🤬 {Fore.CYAN+Style.BRIGHT}[ Fight ]\t\t: {self.player1['name']} ({data[1]['player1']['energy']}) 👀 ({data[1]['player2']['energy']}) {self.player2['name']}")
                elif data[0] == "SET_SUPER_HIT_PREPARE":
                    self.superHit = True
                elif data[0] == "SET_SUPER_HIT_ATTACK_ZONE":
                    content = [
                        "SET_SUPER_HIT_ATTACK_ZONE",
                        {
                            "battleId": self.battleId,
                            "zone": randint(1, 4)
                        }
                    ]
                    await self.websocket.send(f"42{json.dumps(content)}")
                    self.strike['attack'] = True
                elif data[0] == "SET_SUPER_HIT_DEFEND_ZONE":
                    content = [
                        "SET_SUPER_HIT_DEFEND_ZONE",
                        {
                            "battleId": self.battleId,
                            "zone": randint(1, 4)
                        }
                    ]
                    await self.websocket.send(f"42{json.dumps(content)}")
                    self.strike['defense'] = True
                elif data[0] == "ENEMY_LEAVED":
                    return
                elif data[0] == "END":
                    if data[1]['result'] == "WIN":
                        Battle.wins += 1
                        result = f"🔥 ANJAY WIN | Reward: {data[1]['reward']} Coins"
                        print(f"🔥 {Fore.CYAN+Style.BRIGHT}[ Fight ]\t\t: [ Result ] {data[1]['result']} | [ Reward ] {data[1]['reward']} Coins")
                    else:
                        Battle.loses += 1
                        result = f"😹 LOSE BJIR | Reward: {data[1]['reward']} Coins"
                        print(f"😹 {Fore.CYAN+Style.BRIGHT}[ Fight ]\t\t: [ Result ] {data[1]['result']} | [ Reward ] {data[1]['reward']} Coins")
                    
                    # Kirim notifikasi ke Telegram
                    message = f"Battle Result:\n{result}\nWins: {Battle.wins}\nLoses: {Battle.loses}\nBot By @yogakokxd"
                    self.send_telegram_notification(message)
                    
                    await asyncio.sleep(0.5)
                    await self.websocket.recv()
                    self.stop_event.set()
                    return
                try:
                    if ( self.strike['attack'] and not self.strike['defense'] ) or ( self.strike['defense'] and not self.strike['attack'] ):
                        await self.websocket.recv()
                        await self.websocket.recv()
                    if self.strike['attack'] and self.strike['defense']:
                        await self.websocket.recv()
                        await self.websocket.send("3")
                        await self.websocket.recv()

                        self.superHit = False          
                except:
                    pass

    async def connect(self):
        uri = "wss://api-clicker.pixelverse.xyz/socket.io/?EIO=4&transport=websocket"
        async with websockets.connect(uri) as websocket:
            self.websocket = websocket
            data = await websocket.recv()
            content = {
                "tg-id": self.tgId,
                "secret": self.secret,
                "initData": self.initData
            }

            await websocket.send(f"40{json.dumps(content)}")
            await websocket.recv()
            
            data = await websocket.recv()
            data = json.loads(data[2:])
            self.battleId = data[1]['battleId']
            self.player1 = {
                "name": data[1]['player1']['username']
            }
            self.player2 = {
                "name": data[1]['player2']['username']
            }

            print(f"🤪 {Fore.CYAN+Style.BRIGHT}[ Fight Profile ]\t: {Fore.RED+Style.BRIGHT}[ Username ] {data[1]['player1']['username']} {Fore.YELLOW+Style.BRIGHT}| {Fore.GREEN+Style.BRIGHT}[ Level ] {data[1]['player1']['level']} {Fore.YELLOW+Style.BRIGHT}| {Fore.BLUE+Style.BRIGHT}[ Balance ] {split_chunk(str(int(data[1]['player1']['balance'])))} {Fore.YELLOW+Style.BRIGHT}| {Fore.CYAN+Style.BRIGHT}[ Energy ] {split_chunk(str(int(data[1]['player1']['energy'])))} {Fore.YELLOW+Style.BRIGHT}| {Fore.MAGENTA+Style.BRIGHT}[ Damage ] {data[1]['player1']['damage']}")
            print(f"🤪 {Fore.CYAN+Style.BRIGHT}[ Fight Profile ]\t: {Fore.RED+Style.BRIGHT}[ Username ] {data[1]['player2']['username']} {Fore.YELLOW+Style.BRIGHT}| {Fore.GREEN+Style.BRIGHT}[ Level ] {data[1]['player2']['level']} {Fore.YELLOW+Style.BRIGHT}| {Fore.BLUE+Style.BRIGHT}[ Balance ] {split_chunk(str(int(data[1]['player2']['balance'])))} {Fore.YELLOW+Style.BRIGHT}| {Fore.CYAN+Style.BRIGHT}[ Energy ] {split_chunk(str(int(data[1]['player2']['energy'])))} {Fore.YELLOW+Style.BRIGHT}| {Fore.MAGENTA+Style.BRIGHT}[ Damage ] {data[1]['player2']['damage']}")

            for i in range(5, 0, -1):
                print(f"\r⏰ {Fore.YELLOW+Style.BRIGHT}[ Fight ]\t\t: Pertarungan Dimulai Dalam {i} Detik", end="\r", flush=True)
                await asyncio.sleep(1)
            
            print('')
            
            listenerMsgTask = asyncio.create_task(self.listenerMsg())
            hitTask = asyncio.create_task(self.sendHit())

            await asyncio.gather(listenerMsgTask, hitTask)