from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
import json
import asyncio


class EmergencyCenter(Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)

    # TODO:
    # spróbować uruchomić tę klasę "z zewnątrz",
    # tzn. działa sobie program, a ja w terminalu (czy gdzieś indziej)
    # wpisuje miejsce zdarzenia i uruchamia się ta metoda
        
    # dodać licznik eventów (max. 2) i nie pozwalać na dodawanie nowych
    
    # dodać zachowanie, które czeka na wiadomość o zakończeniu zadania
    
    class SendEvent(OneShotBehaviour):
        async def run(self):

            # inicjalizacja zgłoszenia 1
            await asyncio.sleep(2)
            print("\nWysyłanie złoszenia 1 z Centrali...\n")
            event_msg = Message(to="ambulance_coordinator@localhost")
            event_msg.set_metadata("performative", "inform")
            event_msg.set_metadata("ontologia", "traffic-coordination")
            event_msg.set_metadata("language", "event-report")
            event_msg.set_metadata("event_id", "1")
            event_msg.body = json.dumps([18,18])
            await self.send(event_msg)

            # inicjalizacja zgłoszenia 2
            await asyncio.sleep(2)
            print("\nWysyłanie złoszenia 2 z Centrali...\n")
            event_msg = Message(to="ambulance_coordinator@localhost")
            event_msg.set_metadata("performative", "inform")
            event_msg.set_metadata("ontologia", "traffic-coordination")
            event_msg.set_metadata("language", "event-report")
            event_msg.set_metadata("event_id", "2")
            event_msg.body = json.dumps([0,1])
            await self.send(event_msg)


    async def setup(self):
        self.add_behaviour(self.SendEvent())
