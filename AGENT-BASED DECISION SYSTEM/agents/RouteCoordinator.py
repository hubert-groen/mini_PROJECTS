from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
from queue import Queue


class RouteCoordinator(Agent):
    call_id = 0
    destination_x = 0
    destination_y = 0
    last_x = 0
    lats_y = 0
    ambulance_id = 0

    async def setup(self):
        self.add_behaviour(self.GetRouteRequest())

    class GetRouteRequest(OneShotBehaviour):
        async def run(self):
            msg = await self.receive(timeout=3)
            if msg:
                if msg.metadata["language"] == "optimal_route":
                    # @TODO Tutaj bedzie pobranie danych odnosnie zgloszenia
                    agent = self.agent.add_behaviour(self.agent.SendOptimalRoute())
                else:
                    print("Otrzymano nieoczekiwana wiadomosc.")

            await self.agent.stop()

    class SendOptimalRoute(OneShotBehaviour):
        def is_valid(self, x, y):
            return 0 <= x < 20 and 0 <= y < 20

        def find_path(self, start, end):
            queue = Queue()
            visited = set()

            queue.put((start, []))
            visited.add(start)

            while not queue.empty():
                current, path = queue.get()

                x, y = current
                neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

                for neighbor in neighbors:
                    nx, ny = neighbor
                    if self.is_valid(nx, ny) and neighbor not in visited:
                        if neighbor == end:
                            return path + [current, neighbor]

                        queue.put((neighbor, path + [current]))
                        visited.add(neighbor)

            return None

        async def run(self):
            path = self.find_path((self.agent.last_x, self.agent.last_y),
                                  (self.agent.destination_x, self.agent.destination_y))
            recipient = "ambulance_" + self.agent.ambulance_id + "@localhost"
            route_msg = Message(
                to=recipient)
            route_msg.set_metadata("performative", "inform")
            route_msg.set_metadata("ontology", "traffic-coordination")
            route_msg.set_metadata("language", "optimal_route")
            route_msg.body = path
            await self.send(route_msg)

            self.agent.add_behaviour(self.agent.GetAmbulanceGPS())

            await self.agent.stop()  # stop() czy return?
            return  # j.w.

    class GetAmbulanceGPS(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=3)
            if msg:
                if msg.metadata["language"] == "gps_progress":
                    current_x = msg.body[0]
                    current_y = msg.body[1]
                    print("Received GPS data: {}".format(current_x + ", " + current_y))
            else:
                print("No communicates")

            if current_x == self.agent.destination_x and current_y == self.agent.destination_y:  # sprawdzenie, czy karetka jest juz na miejscu
                self.agent.add_behaviour(self.agent.SendRouteFinished())  # Wyslanie info o zakonczeniu przejazdu
                self.agent.last_x = current_x
                self.agent.last_y = current_y
                return  # return czy stop?
            elif current_x != self.agent.destination_x or current_y != self.agent.destination_y:  # sprawdzenie, czy karetka sie przemiescila
                self.agent.last_x = current_x
                self.agent.last_y = current_y
                self.agent.add_behaviour(self.agent.SendTrafficLightsRequest())  # Wyslanie info do koordynatora swiatel

    class SendRouteFinished(OneShotBehaviour):
        async def run(self):
            route_finished_msg = Message(
                to="emergency_center@localhost")
            route_finished_msg.set_metadata("performative", "inform")
            route_finished_msg.set_metadata("ontology", "traffic-coordination")
            route_finished_msg.set_metadata("language", "route_finished")
            route_finished_msg.body = self.agent.call_id
            await self.send(route_finished_msg)

    class SendTrafficLightsRequest(OneShotBehaviour):
        async def run(self):
            traffic_lights_msg = Message(
                to="traffic_lights_coordinator@localhost")
            traffic_lights_msg.set_metadata("performative", "inform")
            traffic_lights_msg.set_metadata("ontology", "traffic-coordination")
            traffic_lights_msg.set_metadata("language", "change_lights")
            traffic_lights_msg.body = (self.agent.last_x, self.agent.last_y)
            await self.send(traffic_lights_msg)
