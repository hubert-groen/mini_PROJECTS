from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


# FIXME:
# wg mnie "zdefiniowane miejsca skrzyżowań" - self.trafficLightsCorditationsList
# powinny być w agencie RouteCoordinator
# i on patrzy, że jeśli karetka jest na tym skrzyżowaniu to wysyła prostą wiadomość
# do trafficcoordinator (zmień tutaj światła)


class TrafficLightCoordinator(Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.trafficLightsCorditationsList = [[9, 5], [1, 1], [2, 2], [1, 3], [8, 4], [0, 2], [7, 3], [4, 0]]

    class GetChangeLightRequest(CyclicBehaviour):
            async def run(self):
                msg = await self.receive()

                if msg and msg.get_metadata("language") == "change_lights":
                    gps_data = msg.body
                    ambulance_id = msg.get_metadata('ambulance_id')
                    if gps_data in self.trafficLightsCorditationsList:
                        print( f"Karetka {ambulance_id} prosi o zmiane swiateł w lokalizacji {gps_data}")
                    else:
                        print( f"Karetka {ambulance_id} prosi o zmiane swiateł w lokalizacji {gps_data} jednak nie ma tam świateł :c")

    async def setup(self):
        self.add_behaviour(self.GetChangeLightRequest())
