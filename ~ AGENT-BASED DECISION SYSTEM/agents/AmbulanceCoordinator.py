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
OBSTACLES_LOCATIONS = []
OBSTACLES_LOCATIONS += [[x, 5] for x in range(12)]
OBSTACLES_LOCATIONS += [[x + 3, 10] for x in range(4)]
OBSTACLES_LOCATIONS += [[16, x + 4] for x in range(3)]
OBSTACLES_LOCATIONS += [[16, x + 10] for x in range(3)]

COLORS = ['green', 'blue', 'bisque1', 'cadetblue1']


class AmbulanceCoordinator(Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)

        self.events_to_be_sent = []

        self.ambulance_1_location = [10, 10]
        self.ambulance_2_location = [11, 11]
        self.ambulance_3_location = [8, 8]
        self.ambulance_4_location = [2, 2]


        self.ambulance_1_free = True
        self.ambulance_2_free = True
        self.ambulance_3_free = True

        self.event_1_location = None
        self.event_2_location = None
        self.event_location_list = []

        self.root = tk.Tk()
        self.root.title("Ambulance Map")
        self.canvas = tk.Canvas(self.root, width=MAP_SIZE * SQUARE_SIZE, height=MAP_SIZE * SQUARE_SIZE)
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.canvas_click_event)

        for i in range(MAP_SIZE + 1):
            self.canvas.create_line(i * SQUARE_SIZE, 0, i * SQUARE_SIZE, MAP_SIZE * SQUARE_SIZE)
            self.canvas.create_line(0, i * SQUARE_SIZE, MAP_SIZE * SQUARE_SIZE, i * SQUARE_SIZE)
            self.root.update()

    def canvas_click_event(self, event):
        self.events_to_be_sent.append(event)

    class SendEvent(CyclicBehaviour):
        def __init__(self):
            super().__init__()

        async def run(self):
            if (len(self.agent.events_to_be_sent) > 0) and (self.agent.ambulance_1_free or self.agent.ambulance_2_free or self.agent.ambulance_3_free):
                receive_event_msg = Message(to="emergency_center@localhost")
                receive_event_msg.set_metadata("language", "receive-event")
                event = self.agent.events_to_be_sent.pop()
                x_coord = math.floor(event.x/SQUARE_SIZE)
                y_coord = math.floor(event.y/SQUARE_SIZE)
                receive_event_msg.set_metadata("x", str(x_coord))
                receive_event_msg.set_metadata("y", str(y_coord))
                await self.send(receive_event_msg)
            

    class Map(CyclicBehaviour):
        def __init__(self):
            super().__init__()
            self.ambulance_1_square = None
            self.ambulance_2_square = None
            self.ambulance_3_square = None
            self.ambulance_4_square = None
            self.event_1_square = None
            self.event_2_square = None
            self.map_obstacles_squares = []

        async def run(self):
            self.update_map()
            self.agent.root.update_idletasks()
            self.agent.root.update()
            self.draw_obstacles()

        def draw_obstacles(self):
            self.map_obstacles_squares = []
            for obstacle in OBSTACLES_LOCATIONS:
                pom = self.draw_square(obstacle, "black")
                self.map_obstacles_squares.append(pom)

        def update_map(self):
            self.delete_all_squares()

            self.ambulance_1_square = self.draw_square(self.agent.ambulance_1_location, "red")
            self.ambulance_2_square = self.draw_square(self.agent.ambulance_2_location, "darkred")
            self.ambulance_3_square = self.draw_square(self.agent.ambulance_3_location, "pink")
            self.ambulance_4_square = self.draw_square(self.agent.ambulance_4_location, "yellow")

            # if self.agent.event_1_location is not None:
            #     self.event_1_square = self.draw_square(self.agent.event_1_location, "green")

            # if self.agent.event_2_location is not None:
            #     self.event_1_square = self.draw_square(self.agent.event_2_location, "yellow")

            if (len(self.agent.event_location_list) > 0):
                for event in self.agent.event_location_list:
                    self.event_1_square = self.draw_square(event, "green")


        def delete_all_squares(self):
            self.agent.canvas.delete(self.ambulance_1_square)
            self.agent.canvas.delete(self.ambulance_2_square)
            self.agent.canvas.delete(self.ambulance_3_square)
            self.agent.canvas.delete(self.ambulance_4_square)
            self.agent.canvas.delete(self.event_1_square)
            self.agent.canvas.delete(self.event_2_square)

        def draw_square(self, position, color):
            x, y = position
            x_pixel = x * SQUARE_SIZE
            y_pixel = y * SQUARE_SIZE
            return self.agent.canvas.create_rectangle(x_pixel, y_pixel, x_pixel + SQUARE_SIZE, y_pixel + SQUARE_SIZE, fill=color)

    class GetEvent(CyclicBehaviour):
        '''
        1. oczekiwanie na otrzymanie zgłoszenia (z centrali)
        2. wybranie najbliższej oraz wolnej karetki (na podstawie danych GPS)
        3. wysłanie requestu do konkretnej karetki
        4. uruchomienie zachowania GetRequestFromAmbulance
        '''

        def find_closest_ambulance(self, event_location):      

            ambulances = [
                (1, math.sqrt((self.agent.ambulance_1_location[0] - event_location[0])**2 +
                            (self.agent.ambulance_1_location[1] - event_location[1])**2),
                self.agent.ambulance_1_free),
                (2, math.sqrt((self.agent.ambulance_2_location[0] - event_location[0])**2 +
                            (self.agent.ambulance_2_location[1] - event_location[1])**2),
                self.agent.ambulance_2_free),
                (3, math.sqrt((self.agent.ambulance_3_location[0] - event_location[0])**2 +
                            (self.agent.ambulance_3_location[1] - event_location[1])**2),
                self.agent.ambulance_3_free)
            ]

            ambulances = [(num, distance) for num, distance, is_free in ambulances if is_free]
            sorted_ambulances = sorted(ambulances, key=lambda x: x[1])

            return [ambulance[0] for ambulance in sorted_ambulances]


        async def run(self):

            # 1
            get_event_msg = await self.receive()
            if get_event_msg and get_event_msg.get_metadata('language') == "event-report":
                event_location = json.loads(get_event_msg.body)
                event_id = get_event_msg.get_metadata('event_id')
                setattr(self.agent, f"event_{event_id}_location", event_location)
                self.agent.event_location_list.append(event_location)

                # 2               
                closest_ambulance = self.find_closest_ambulance(event_location)

                if len(closest_ambulance) > 0:

                    print('Koordynator dostał nowe zgłoszenie - najbliższa karetka: {}\n'.format(closest_ambulance[0]))

                    # 3
                    request_amb_msg = Message(to=f"ambulance_{closest_ambulance[0]}@localhost")
                    request_amb_msg.set_metadata("performative", "request")
                    request_amb_msg.set_metadata("ontologia", "traffic-coordination")
                    request_amb_msg.set_metadata("language", "event-request")
                    request_amb_msg.body = json.dumps(event_location)
                    await self.send(request_amb_msg)

                    # 4
                    self.agent.add_behaviour(self.agent.GetRequestFromAmbulance(event_id, event_location, closest_ambulance))
                
                else:
                    print("Wszystkie karetki są zajęte!")

    class GetRequestFromAmbulance(OneShotBehaviour):
        '''
        1. oczekiwanie na odpowiedź akceptacji zgłoszenia od karetki
        2. request do koordynatora przejazdu o wyznaczenie najlepszej trasy
        3. uruchomienie zachowania UpdateRideProgress
        4. brak odpowiedzi od karetki: wysłanie wiadomości do kolejnej najbliższej i uruchomienie zachowania GetRequestFromAmbulance
        '''
        def __init__(self, event_id, event_location, closest_ambulance):
            super().__init__()
            self.event_id = event_id
            self.event_location = event_location
            self.closest_list = closest_ambulance
            self.ambulance_id = closest_ambulance[0]
        
        async def run(self):

            # 1
            answer_amb_msg = await self.receive(timeout=5)
            if answer_amb_msg and answer_amb_msg.get_metadata('language') == 'request-answer':
                answer = json.loads(answer_amb_msg.body)

                print(f'Karetka {self.ambulance_id} potwierdziła przyjęcie zgłoszenia.\n')

                setattr(self.agent, f"ambulance_{self.ambulance_id}_free", False)

                # 2
                request_route_msg = Message(to="route_coordinator@localhost")
                request_route_msg.set_metadata("performative", "request")
                request_route_msg.set_metadata("ontologia", "traffic-coordination")
                request_route_msg.set_metadata("language", "path-request")

                path_request_data = {
                    "event_id": self.event_id,
                    "ambulance_id": self.ambulance_id,
                    "ambulance_location": getattr(self.agent, f"ambulance_{self.ambulance_id}_location"),
                    "event_location": self.event_location
                }

                request_route_msg.body = json.dumps(path_request_data)
                await self.send(request_route_msg)

                # 3
                self.agent.add_behaviour(self.agent.UpdateRideProgress(self.ambulance_id, self.event_id, self.event_location))

            # 4
            else:
                self.closest_list.pop(0)

                if len(self.closest_list) > 0:

                    print(f'Brak odpowiedzi od karetki {self.ambulance_id} - kolejna najbliższa: {self.closest_list[0]}\n')

                    request_amb_msg = Message(to=f"ambulance_{self.closest_list[0]}@localhost")
                    request_amb_msg.set_metadata("performative", "request")
                    request_amb_msg.set_metadata("ontologia", "traffic-coordination")
                    request_amb_msg.set_metadata("language", "event-request")
                    request_amb_msg.body = json.dumps(self.event_location)
                    await self.send(request_amb_msg)

                    self.agent.add_behaviour(self.agent.GetRequestFromAmbulance(self.event_id, self.event_location, self.closest_list))

                else:
                    print('Żadna karetka nie odpowiedziała.')


    class UpdateRideProgress(CyclicBehaviour):
        '''
        1. przesyłanie aktualnego GPS karetki (do koordynatora przejazdu)
        
        w przypadku zakończonego przejazdu:
        2. wysłanie powiadomienia do route coordinator
        3. wysłanie powiadomienia do emergency center
        4. ustawienie statusu karetki na free = True
        '''
        def __init__(self, ambulance_id, event_id, event_location):
            super().__init__()
            self.ambulance_id = ambulance_id
            self.event_id = event_id
            self.event_location = event_location

        async def run(self):

            # 1
            update_ride_msg = Message(to="route_coordinator@localhost")
            update_ride_msg.set_metadata("performative", "inform")
            update_ride_msg.set_metadata("ontologia", "traffic-coordination")
            update_ride_msg.set_metadata("language", "gps-progress")
            update_ride_msg.set_metadata("ambulance_id", f"{self.ambulance_id}")

            current_location = getattr(self.agent, f"ambulance_{self.ambulance_id}_location", None)

            if current_location != self.event_location:
                update_ride_msg.body = json.dumps(current_location)          
                await self.send(update_ride_msg)
                await asyncio.sleep(2)

            else:
                setattr(self.agent, f"event_{self.event_id}_location", None)
                
                # 2
                update_ride_msg.set_metadata("language", "gps-progress-finished")
                await self.send(update_ride_msg)

                # 3
                finish_event_msg = Message(to="emergency_center@localhost")
                finish_event_msg.set_metadata("performative", "inform")
                finish_event_msg.set_metadata("ontologia", "traffic-coordination")
                finish_event_msg.set_metadata("language", "event-finish")
                finish_event_msg.set_metadata("event_id", str(self.event_id))
                await self.send(finish_event_msg)
                self.agent.event_location_list.remove(current_location)
                # 4
                print(f'Karetka {self.ambulance_id} zrealizowała zlecenie.')
                setattr(self.agent, f"ambulance_{self.ambulance_id}_free", True)
                
                self.kill()

    class GetAmbulanceGPS(CyclicBehaviour):
        '''
        odbieranie aktualnego GPS karetki - działa cały czas w tle
        '''
        async def run(self):
            msg = await self.receive()

            if msg and msg.get_metadata("language") == "gps":
                gps_data = json.loads(msg.body)
                ambulance_id = msg.get_metadata('ambulance_id')
                location_variable = f"ambulance_{ambulance_id}_location"
                setattr(self.agent, location_variable, gps_data)

    class PrintData(CyclicBehaviour):
        '''
        funkcja pomocnicza do wyświetlania pozycji GPS w terminalu
        '''
        async def run(self):

            print(f"Ambulance 1 = {self.agent.ambulance_1_location}")
            print(f"Ambulance 2 = {self.agent.ambulance_2_location}")
            print(f"Ambulance 3 = {self.agent.ambulance_3_location}")
            print('\n')

            await asyncio.sleep(1)

    async def setup(self):
        self.add_behaviour(self.Map())
        self.add_behaviour(self.GetEvent())
        self.add_behaviour(self.GetAmbulanceGPS())
        self.add_behaviour(self.PrintData())
        self.add_behaviour(self.SendEvent())