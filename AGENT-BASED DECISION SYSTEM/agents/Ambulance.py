from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
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
        '''
        1. oczekiwanie na otrzymanie zgłoszenia (od koordynatora karetek)
        2. odpowiedź potwierdzająca przyjęcie zgłoszenia (do koordynatora karetek)
        3. uruchomienie zachowania GetRoute (oczekiwanie na trasę przejazdu)
        '''
        async def run(self):

            # 1
            request_msg = await self.receive()
            if request_msg and request_msg.get_metadata('language') == 'event-request':
                event_location = json.loads(request_msg.body)
                print('karetka otrzymuje request')

                # 2
                answer_msg = Message(to=f"ambulance_coordinator@localhost")
                answer_msg.set_metadata("performative", "confirm")
                answer_msg.set_metadata("ontologia", "traffic-coordination")
                answer_msg.set_metadata("language", "request-answer")
                answer_msg.body = json.dumps('yes')
                await self.send(answer_msg)
                print('karetka odpowiada yes')

                # 3
                self.agent.add_behaviour(self.agent.GetRoute())


    class GetRoute(CyclicBehaviour):
        '''
        1. oczekiwanie na otrzymanie trasy przejazdu (od koordynatora przejazdu)
        2. uruchomienie zachowania Drive
        '''
        def __init__(self):
            super().__init__()

        async def run(self):

            # 1
            path_msg = await self.receive()
            if path_msg and path_msg.get_metadata("language") == "optimal-route":
            
                optimal_path = json.loads(path_msg.body)

                print('karetka dostała trasę:')
                print(optimal_path)
                print("---------------")

                print(f"Karetka {self.agent.ambulance_id} zaczyna jechać...")

                # 2
                self.agent.add_behaviour(self.agent.Drive(optimal_path))


    class SendGPS(CyclicBehaviour):
        '''
        przesyłanie aktualnego GPS karetki - działa cały czas w tle
        '''
        async def run(self):
            msg = Message(to="ambulance_coordinator@localhost")
            msg.set_metadata("performative", "inform")
            msg.set_metadata("ontologia", "traffic-coordination")
            msg.set_metadata("language", "gps")
            msg.set_metadata("ambulance_id", f"{self.agent.ambulance_id}")

            msg.body = json.dumps(self.agent.ambulance_position)

            await self.send(msg)
            await asyncio.sleep(2)


    class Drive(OneShotBehaviour):
        '''
        symulacja jazdy karetki - zmiana GPS punkt po punkcie, według wyznaczonej trasy
        '''
        def __init__(self, path):
            super().__init__()
            self.path = path

        async def run(self):
            print('karetka zaczyna jechać')
            for position in self.path:
                self.agent.ambulance_position = position
                await asyncio.sleep(2)         

            # TODO: tutaj trzeba dodać że zakończone i przesłać jakiś komunikat   


    async def setup(self):
        self.add_behaviour(self.NewTask())
        self.add_behaviour(self.SendGPS())