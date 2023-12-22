from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
import json
import asyncio


class EmergencyCenter(Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)

        self.some_event_location = [18,18]

    # TODO:
    # spróbować uruchomić tę klasę "z zewnątrz",
    # tzn. działa sobie program, a ja w terminalu (czy gdzieś indziej)
    # wpisuje miejsce zdarzenia i uruchamia się ta metoda
    class SendEvent(OneShotBehaviour):
        async def run(self):

            await asyncio.sleep(2)
            print("\nWysyłanie złoszenia z Centrali...\n")

            event_msg = Message(to="ambulance_coordinator@localhost")
            event_msg.set_metadata("performative", "inform")
            event_msg.set_metadata("ontologia", "traffic-coordination")
            event_msg.set_metadata("language", "event-report")
            event_msg.set_metadata("event_id", "1")

            event_msg.body = json.dumps(self.agent.some_event_location)

            await self.send(event_msg)

    async def setup(self):
        self.add_behaviour(self.SendEvent())



# class EmergencyCenter(Agent):

#     class SendEvent(OneShotBehaviour):
#         async def run(self):
#             print("Request sent from EmergencyCenter")
#             event_msg = Message(to="ambulance_coordinator@localhost")
#             event_msg.set_metadata("m_type", "m_event")
#             event_msg.body = "Mokotow"

#             await self.send(event_msg)

#             # await self.agent.stop()

#     class SendRouteRequest(OneShotBehaviour):
#         async def run(self):
#             # msg.metadata["MSG_TYPE"] == "ROUTE_REQUEST"
#             msg = Message(to="route_coordinator@localhost")
#             msg.set_metadata("MSG_TYPE", "ROUTE_REQUEST")
#             msg.body = "Ambulance to Mokotow"
#             await self.send(msg)

#     class GetRideEndInfo(OneShotBehaviour):
#         async def run(self):
#             msg = await self.receive(timeout=3)
#             if msg.metadata["MSG_TYPE"] == "ROUTE_FINISHED":
#                 print("Ambulance finished ride!")

#     class GetAmbulanceID(OneShotBehaviour):
#         async def run(self):
#             msg = await self.receive(timeout=3)
#             if msg.metadata["MSG_TYPE"] == "AMBULANCE_ID":
#                 print("Sending route request!")
#                 self.agent.add_behaviour(self.agent.SendRouteRequest())

#     async def setup(self):
#         self.add_behaviour(self.SendEvent())
