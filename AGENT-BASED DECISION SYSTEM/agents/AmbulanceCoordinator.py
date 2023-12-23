from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
import asyncio
import math
import tkinter as tk
import json

# Ustawienia mapy
MAP_SIZE = 20
SQUARE_SIZE = 30
WINDOW_SIZE = MAP_SIZE * SQUARE_SIZE


class AmbulanceCoordinator(Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)

        self.ambulance_1_location = [9, 9]
        self.ambulance_2_location = [10, 10]

        self.event_1_location = False
        self.event_2_location = False

        self.root = tk.Tk()
        self.root.title("Ambulance Map")
        self.canvas = tk.Canvas(self.root, width=MAP_SIZE * SQUARE_SIZE, height=MAP_SIZE * SQUARE_SIZE)
        self.canvas.pack()

        for i in range(MAP_SIZE + 1):
            self.canvas.create_line(i * SQUARE_SIZE, 0, i * SQUARE_SIZE, MAP_SIZE * SQUARE_SIZE)
            self.canvas.create_line(0, i * SQUARE_SIZE, MAP_SIZE * SQUARE_SIZE, i * SQUARE_SIZE)
            self.root.update()

    class Map(CyclicBehaviour):
        def __init__(self):
            super().__init__()
            self.ambulance_2_square = None
            self.ambulance_1_square = None

        async def run(self):
            self.update_map()
            self.agent.root.update_idletasks()
            self.agent.root.update()

        def update_map(self):
            self.delete_all_squares()
            self.ambulance_1_square = self.draw_square(self.agent.ambulance_1_location, "red")
            self.ambulance_2_square = self.draw_square(self.agent.ambulance_2_location, "blue")

        def delete_all_squares(self):
            self.agent.canvas.delete(self.ambulance_1_square)
            self.agent.canvas.delete(self.ambulance_2_square)

        def draw_square(self, position, color):
            x, y = position
            x_pixel = x * SQUARE_SIZE
            y_pixel = y * SQUARE_SIZE
            return self.agent.canvas.create_rectangle(x_pixel, y_pixel, x_pixel + SQUARE_SIZE, y_pixel + SQUARE_SIZE, fill=color)

    
    class ManageEvent(CyclicBehaviour):

            # tutaj trzeba też będzie sprawdzić czy są zajęte
        def find_closest_ambulance(self, event_location):
            distance_ambulance_1 = math.sqrt((self.agent.ambulance_1_location[0] - event_location[0])**2 +
                                            (self.agent.ambulance_1_location[1] - event_location[1])**2)

            distance_ambulance_2 = math.sqrt((self.agent.ambulance_2_location[0] - event_location[0])**2 +
                                            (self.agent.ambulance_2_location[1] - event_location[1])**2)

            if distance_ambulance_1 < distance_ambulance_2:
                return 1
            else:
                return 2

        async def run(self):
            get_event_msg = await self.receive()

            if get_event_msg and get_event_msg.get_metadata('language') == "event-report":
                event_location = json.loads(get_event_msg.body)
                event_id = get_event_msg.get_metadata('event_id')
                location_variable = f"event_{event_id}_location"
                setattr(self.agent, location_variable, event_location)                
                closest_ambulance = self.find_closest_ambulance(event_location)
                print('Koordynator dostał nowe zgłoszenie - najbliższa karetka: {}\n'.format(closest_ambulance))

                request_route_msg = Message(to="route_coordinator@localhost")
                request_route_msg.set_metadata("performative", "request")
                request_route_msg.set_metadata("ontologia", "traffic-coordination")
                request_route_msg.set_metadata("language", "path-request")

                path_request_data = {
                    "event_id": event_id,
                    "ambulance_id": closest_ambulance,
                    "ambulance_location": getattr(self.agent, f"ambulance_{closest_ambulance}_location"),
                    "event_location": event_location
                }

                request_route_msg.body = json.dumps(path_request_data)
                await self.send(request_route_msg)

                # region
                # # wysłanie wiadomości do karetki
                # request_msg = Message(to=f"ambulance_{closest_ambulance}@localhost")
                # request_msg.set_metadata("performative", "request")
                # request_msg.set_metadata("ontologia", "traffic-coordination")
                # request_msg.set_metadata("language", "event-request")
                # request_msg.body = json.dumps(event_location)
                # await self.send(request_msg)
            
                # # tutaj zmienić, że jak nie dostanę odp. to zamykam to i wysyłam do drugiej karetki
                # accept_msg = await self.receive()

                # if accept_msg and accept_msg.get_metadata('language') == 'request-answer':

                #     answer = json.loads(accept_msg.body)

                #     # wysłanie wiadomości do koordynatora przejazdu
                #     # c_msg = Message(to=f"traffic_coordinator@localhost")      # FIXME: inna nazwa
                #     # c_msg.set_metadata("performative", "request")
                #     # c_msg.set_metadata("ontologia", "traffic-coordination")
                #     # c_msg.set_metadata("language", "path-request")
                #     # # FIXME: w body będzie id zdarzenia, id karetki, pozycja karetki, pozycja zdarzenia
                #     # await self.send(c_msg)
                #     # print('wyslana prośba przejazdu')
                # endregion
            

    class GetAmbulanceGPS(CyclicBehaviour):
        async def run(self):
            msg = await self.receive()

            if msg and msg.get_metadata("language") == "gps":
                gps_data = json.loads(msg.body)
                ambulance_id = msg.get_metadata('ambulance_id')
                location_variable = f"ambulance_{ambulance_id}_location"
                setattr(self.agent, location_variable, gps_data)

    # to będzie do wyrzucenia, bo to tylko printuje pozycje które są na mapie
    class PrintData(CyclicBehaviour):
        async def run(self):

            print(f"Ambulance 1 = {self.agent.ambulance_1_location}")
            print(f"Ambulance 2 = {self.agent.ambulance_2_location}")
            print('\n')

            await asyncio.sleep(1)

    async def setup(self):
        self.add_behaviour(self.Map())
        self.add_behaviour(self.GetAmbulanceGPS())
        self.add_behaviour(self.ManageEvent())
        self.add_behaviour(self.PrintData())