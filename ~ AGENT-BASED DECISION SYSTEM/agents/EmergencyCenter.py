from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
import json
import asyncio


class EmergencyCenter(Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.event_list = [False, False]
        self.event_counter = 3

    # TODO:
    # inicjalizacja zdarzenia z zewnątrz (np. max 2 at the same time)

    class SendEvent(OneShotBehaviour):
        async def run(self):
            pass
            # inicjalizacja zgłoszenia 1
            # await asyncio.sleep(2)
            # print("\nWysyłanie złoszenia 1 z Centrali...\n")
            # event_msg = Message(to="ambulance_coordinator@localhost")
            # event_msg.set_metadata("performative", "inform")
            # event_msg.set_metadata("ontologia", "traffic-coordination")
            # event_msg.set_metadata("language", "event-report")
            # event_msg.set_metadata("event_id", "1")
            # self.agent.event_list[0] = True
            # event_msg.body = json.dumps([1,1])
            # await self.send(event_msg)
            # self.agent.add_behaviour(self.agent.FinishEvent(1))


            # # inicjalizacja zgłoszenia 2
            # await asyncio.sleep(5)
            # print("\nWysyłanie złoszenia 2 z Centrali...\n")
            # event_msg = Message(to="ambulance_coordinator@localhost")
            # event_msg.set_metadata("performative", "inform")
            # event_msg.set_metadata("ontologia", "traffic-coordination")
            # event_msg.set_metadata("language", "event-report")
            # event_msg.set_metadata("event_id", "2")
            # self.agent.event_list[1] = True
            # event_msg.body = json.dumps([2,2])
            # await self.send(event_msg)
            # self.agent.add_behaviour(self.agent.FinishEvent(2))

    class ReceiveEvent(CyclicBehaviour):
        async def run(self):
            msg = await self.receive()
            if msg and msg.get_metadata("language") == "receive-event":
                print("New event! Location: x: ", msg.get_metadata("x"), ", y: ", msg.get_metadata("y"))            
                event_msg = Message(to="ambulance_coordinator@localhost")
                event_msg.set_metadata("performative", "inform")
                event_msg.set_metadata("ontologia", "traffic-coordination")
                event_msg.set_metadata("language", "event-report")
                event_msg.set_metadata("event_id", str(self.agent.event_counter))
                self.agent.event_counter += 1
                self.agent.event_list.append(True)
                event_msg.body = json.dumps([int(msg.get_metadata("x")), int(msg.get_metadata("y"))])
                await self.send(event_msg)

    class FinishEvent(CyclicBehaviour):
        def __init__(self, event_id):
            super().__init__()
            self.event_id = event_id
        '''
        1. oczekiwanie na wiadomość o zakończeniu przejazdu (obsłużenie zgłoszenia)
        2. zamknięcie zachowania FinishEvent, jeśli żadne zgłoszenie nie jest aktywne
        '''

        async def run(self):

            # 1
            msg = await self.receive()
            if msg and msg.get_metadata("language") == "event-finish" and msg.get_metadata("event_id") == str(self.event_id):

                self.agent.event_list[self.event_id - 1] = False
                print(f'Zgłoszenie nr {self.event_id} zostało zrealizowane.')

                # 2
                if all(value is False for value in self.agent.event_list):
                    self.kill()

    async def setup(self):
        self.add_behaviour(self.SendEvent())
        self.add_behaviour(self.ReceiveEvent())
