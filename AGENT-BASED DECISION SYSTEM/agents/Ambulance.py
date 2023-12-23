from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import json
import asyncio
import random

class Ambulance(Agent):
    def __init__(self, jid, password, ambulance_id, initial_position):
        super().__init__(jid, password)

        self.ambulance_id = ambulance_id
        self.ambulance_position = initial_position

        self.accepted_task = False
        self.destination_path = False

    class NewTask(CyclicBehaviour):
        async def run(self):
            msg = await self.receive()
            if msg and msg.get_metadata('language') == "event-request":
                event_location = json.loads(msg.body)

                answer_msg = Message(to=f"ambulance_coordinator@localhost")
                answer_msg.set_metadata("performative", "confirm")
                answer_msg.set_metadata("ontologia", "traffic-coordination")
                answer_msg.set_metadata("language", "request-answer")
                answer_msg.body = json.dumps('yes')
                await self.send(answer_msg)

                self.agent.accepted_task = True

                #TODO: path_msg = await self.receive()

                print(f"Karetka {self.agent.ambulance_id} zaczyna jechać...")
                self.agent.add_behaviour(self.agent.Drive())



    # update w tle cały czas - nie trzeba nic zmieniać
    class SendGPS(CyclicBehaviour):
        async def run(self):
            msg = Message(to="ambulance_coordinator@localhost")
            msg.set_metadata("performative", "inform")
            msg.set_metadata("ontologia", "traffic-coordination")
            msg.set_metadata("language", "gps")
            msg.set_metadata("ambulance_id", f"{self.agent.ambulance_id}")

            msg.body = json.dumps(self.agent.ambulance_position)

            await self.send(msg)
            await asyncio.sleep(2)


    class Drive(CyclicBehaviour):
        async def run(self):
            direction = random.choice(["up", "down", "left", "right"])

            if direction == "up" and self.agent.ambulance_position[0] > 0:
                self.agent.ambulance_position[0] -= 2
            elif direction == "down" and self.agent.ambulance_position[0] < 19:
                self.agent.ambulance_position[0] += 2
            elif direction == "left" and self.agent.ambulance_position[1] > 0:
                self.agent.ambulance_position[1] -= 2
            elif direction == "right" and self.agent.ambulance_position[1] < 19:
                self.agent.ambulance_position[1] += 2

            await asyncio.sleep(1)
            

    async def setup(self):
        self.add_behaviour(self.NewTask())
        self.add_behaviour(self.SendGPS())