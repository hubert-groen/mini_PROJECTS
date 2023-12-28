from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
from queue import Queue
import json


class RouteCoordinator(Agent):

    class GetRouteRequest(CyclicBehaviour):
        '''
        1. oczekiwanie na prośbę wyznaczenia najlepszej trasy (od koordynatora karetek)
        2. uruchomienie zachowania SendOprimalRoute
        '''
        async def run(self):

            # 1
            request_route_msg = await self.receive()
            if request_route_msg and request_route_msg.get_metadata("language") == "path-request":

                    path_request_data = json.loads(request_route_msg.body)
                    print('Koordynator przejazdu dostał prośbę')
                    print(path_request_data)
                    print("--------------")

                    # 2
                    self.agent.add_behaviour(self.agent.SendOptimalRoute(path_request_data))


    class SendOptimalRoute(OneShotBehaviour):
        '''
        1. znalezienie najlepszej trasy
        2. wysłanie jej do karetki
        '''
        def __init__(self, path_request_data):
            super().__init__()
            self.path_request_data = path_request_data
            self.event_id = path_request_data.get("event_id")
            self.ambulance_id = path_request_data.get("ambulance_id")

            event_location = path_request_data.get("event_location")
            self.destination_x = event_location[0]
            self.destination_y = event_location[1]

            ambulance_location = path_request_data.get("ambulance_location")
            self.start_x = ambulance_location[0]
            self.start_y = ambulance_location[1]

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

            # 1
            path = self.find_path((self.start_x, self.start_y), (self.destination_x, self.destination_y))

            # 2
            recipient = "ambulance_" + str(self.ambulance_id) + "@localhost"
            route_msg = Message(to=recipient)
            route_msg.set_metadata("performative", "inform")
            route_msg.set_metadata("ontology", "traffic-coordination")
            route_msg.set_metadata("language", "optimal-route")
            print(f"path: {path}")
            route_msg.body = json.dumps(path)
            await self.send(route_msg)

            self.agent.add_behaviour(self.agent.GetAmbulanceGPS(str(self.ambulance_id)))
            self.kill()

    class GetAmbulanceGPS(CyclicBehaviour):
        def __init__(self, amb_id):
            super().__init__()
            self.ambulance_id = amb_id
        '''
        1. oczekiwanie na aktualną pozycję karetki (od koordynatora karetek)
        2. wysłanie requestu zmiany świateł (do koordynatora przejazdu)
        '''
        async def run(self):
            # 1
            msg = await self.receive()
            if msg and msg.metadata["language"] == "gps-progress" and msg.metadata["ambulance_id"] == self.ambulance_id:
                traffic_lights_msg = Message(
                    to="traffic_light_coordinator@localhost")
                traffic_lights_msg.set_metadata("performative", "inform")
                traffic_lights_msg.set_metadata("ontology", "traffic-coordination")
                traffic_lights_msg.set_metadata("language", "change_lights")
                traffic_lights_msg.set_metadata("ambulance_id", self.ambulance_id)
                traffic_lights_msg.body = msg.body # ma byc stringiem
                await self.send(traffic_lights_msg)
                print("Received GPS data: {}".format(msg.body))

            elif msg and msg.metadata["language"] == "gps-progress-end" and msg.metadata["ambulance_id"] == self.ambulance_id:
                self.kill()

    async def setup(self):
        self.add_behaviour(self.GetRouteRequest())
