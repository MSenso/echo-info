import asyncio
import json
import random
from typing import List

from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.Initiator = False
        self.Engaged = False
        self.N = 0
        self.load = random.randint(0, 100) if node_id != 0 else 0
        self.Pred = None
        self.neighbors: List[Node] = []

    async def receive_message(self, sender, websocket: WebSocket):
        if not self.Engaged:
            await websocket.send_text(str(self))
            await asyncio.sleep(1)
            self.Engaged = True
            self.N = 0
            self.Pred: Node = sender
            for neighbor in self.neighbors:
                if neighbor != sender:
                    await neighbor.receive_message(self, websocket)
                    self.N += 1
            await self.Pred.receive_echo_message(self, websocket)

    async def receive_echo_message(self, sender, websocket: WebSocket):
        self.N += 1
        if self.N == len(list(filter(lambda x: x.id != sender.id, self.neighbors))):
            if not self.Initiator:
                await self.Pred.receive_echo_message(self, websocket)
            else:
                await websocket.send_text(f"Эхо для узла № {self.id}")
                await asyncio.sleep(1)

    async def start_explorer_wave(self, websocket: WebSocket):
        if not self.Engaged:
            self.Initiator = True
            self.Engaged = True
            for neighbor in self.neighbors:
                if not neighbor.Engaged:
                    await neighbor.receive_message(self, websocket)

    async def run_algorithm(self, websocket: WebSocket):
        self.Initiator = True
        await self.start_explorer_wave(websocket)

    def __str__(self):
        return f"Вычислительный узел №{self.id}: Нагрузка {self.load}%"


class Topology(BaseModel):
    items: dict[int, List[int]]


@app.websocket("/")
async def root(websocket: WebSocket):
    await websocket.accept()
    json_data = await websocket.receive_text()

    # Parse JSON data into dictionary
    items = json.loads(json.loads(json_data))['items']
    result = {item['id']: [int(x.strip()) for x in item['items']] for item in items}
    logging.info(result)

    # Receive second message (integer value)
    int_value = await websocket.receive_text()

    # Parse integer value into integer
    int_value = int(int_value)
    nodes = {}
    for node_id in result.keys():
        nodes[node_id] = Node(node_id)

    for node_id, neighbors in result.items():
        for neighbor_id in neighbors:
            nodes[node_id].neighbors.append(nodes[neighbor_id])

    await nodes[int_value].run_algorithm(websocket)
