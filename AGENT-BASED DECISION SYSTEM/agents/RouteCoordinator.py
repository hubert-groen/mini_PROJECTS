from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
from queue import Queue
import json


class RouteCoordinator(Agent):

    # otrzymanie prośby wyznaczenia najlepszej trasy
    class GetRouteRequest(CyclicBehaviour):
        '''
        otrzymanie prośby wyznaczenia najlepszej trasy od koordynatora karetek
        '''
        async def run(self):
            request_route_msg = await self.receive()
            if request_route_msg and request_route_msg.get_metadata("language") == "path-request":
                    
                    path_request_data = json.loads(request_route_msg.body)
                    print('route dostał prośbę')
                    print(path_request_data)
                    print("--------------")
                    self.agent.add_behaviour(self.agent.SendOptimalRoute(path_request_data))

    # znalezienie najlepszej trasy
    # wysłanie jej do karetki
    #
    class SendOptimalRoute(OneShotBehaviour):
        '''
        - znalezienie najlepszej trasy
        - wysłanie jej do karetki
        
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
            path = self.find_path((self.start_x, self.start_y), (self.destination_x, self.destination_y))
            recipient = "ambulance_" + str(self.ambulance_id) + "@localhost"
            route_msg = Message(to=recipient)
            route_msg.set_metadata("performative", "inform")
            route_msg.set_metadata("ontology", "traffic-coordination")
            route_msg.set_metadata("language", "optimal-route")
            print(f"path: {path}")
            route_msg.body = json.dumps(path)
            await self.send(route_msg)


            # TODO: TUTAJ BĘDZIE
            # - wysłanie trasy (body = path) do karetki - DONE
            # pobieranie GPS is przełączanie świateł + zakończenie zadania

            # self.agent.add_behaviour(self.agent.GetAmbulanceGPS())

            # FIXME: wg mnie nie robimy nigdzie agent stop, ponieważ wtedy cały system padnie
            # await self.agent.stop()  # stop() czy return?
            # return  # j.w.

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


    async def setup(self):
        self.add_behaviour(self.GetRouteRequest())