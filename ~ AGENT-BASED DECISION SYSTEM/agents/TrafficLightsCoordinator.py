from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

class TrafficLightCoordinator(Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)

    class GetChangeLightRequest(CyclicBehaviour):
            async def run(self):
                msg = await self.receive()

                if msg and msg.get_metadata("language") == "change-lights":
                    gps_data = msg.body
                    ambulance_id = msg.get_metadata('ambulance_id')
                    print(f"Karetka {ambulance_id} prosi o zmiane swiateł w lokalizacji {gps_data}")

    async def setup(self):
        self.add_behaviour(self.GetChangeLightRequest())