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

        self.ambulance_1_location = [10, 10]
        self.ambulance_2_location = [11, 11]

        self.event_1_location = None
        self.event_2_location = None

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
            self.event_1_square = None
            self.event_2_square = None

        async def run(self):
            self.update_map()
            self.agent.root.update_idletasks()
            self.agent.root.update()

        def update_map(self):
            self.delete_all_squares()

            self.ambulance_1_square = self.draw_square(self.agent.ambulance_1_location, "red")
            self.ambulance_2_square = self.draw_square(self.agent.ambulance_2_location, "blue")

            if self.agent.event_1_location is not None:
                self.event_1_square = self.draw_square(self.agent.event_1_location, "green")

            if self.agent.event_2_location is not None:
                self.event_1_square = self.draw_square(self.agent.event_2_location, "yellow")

        def delete_all_squares(self):
            self.agent.canvas.delete(self.ambulance_1_square)
            self.agent.canvas.delete(self.ambulance_2_square)
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
        2. wybranie najbliższej karetki (na podstawie danych GPS)
        3. wysłanie requestu do konkretnej karetki
        4. uruchomienie zachowania GetRequestFromAmbulance
        '''

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

            # 1
            get_event_msg = await self.receive()
            if get_event_msg and get_event_msg.get_metadata('language') == "event-report":
                event_location = json.loads(get_event_msg.body)
                event_id = get_event_msg.get_metadata('event_id')
                # location_variable = f"event_{event_id}_location"
                setattr(self.agent, f"event_{event_id}_location", event_location)

                # 2               
                closest_ambulance = self.find_closest_ambulance(event_location)
                print('Koordynator dostał nowe zgłoszenie - najbliższa karetka: {}\n'.format(closest_ambulance))

                # 3
                request_amb_msg = Message(to=f"ambulance_{closest_ambulance}@localhost")
                request_amb_msg.set_metadata("performative", "request")
                request_amb_msg.set_metadata("ontologia", "traffic-coordination")
                request_amb_msg.set_metadata("language", "event-request")
                request_amb_msg.body = json.dumps(event_location)
                print('wysłanie prośby do karetki')
                await self.send(request_amb_msg)

                # 4
                self.agent.add_behaviour(self.agent.GetRequestFromAmbulance(event_id, event_location, closest_ambulance))


    class GetRequestFromAmbulance(CyclicBehaviour):
        '''
        1. oczekiwanie na odpowiedź akceptacji zgłoszenia od karetki
        2. request do koordynatora przejazdu o wyznaczenie najlepszej trasy
        3. uruchomienie zachowania UpdateRideProgress
        '''
        def __init__(self, event_id, event_location, closest_ambulance):
            super().__init__()
            self.event_id = event_id
            self.event_location = event_location
            self.ambulance_id = closest_ambulance
        
        async def run(self):

            # 1
            answer_amb_msg = await self.receive()
            if answer_amb_msg and answer_amb_msg.get_metadata('language') == 'request-answer':
                answer = json.loads(answer_amb_msg.body)                    # narazie zakładamy, że odpowiedź to zawsze 'yes'
                print(f'koordynator dostał odp. od karetki: {answer}')

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
                self.agent.add_behaviour(self.agent.UpdateRideProgress(self.ambulance_id, self. event_id, self.event_location))
                self.kill()


    class UpdateRideProgress(CyclicBehaviour):
        '''
        1. przesyłanie aktualnego GPS karetki (do koordynatora przejazdu)
        
        w przypadku zakończonego przejazdu:
        2. wysłanie powiadomienia do route coordinator
        3. wysłanie powiadomienia do emergency center
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
            print('\n')

            await asyncio.sleep(1)


    async def setup(self):
        self.add_behaviour(self.Map())
        self.add_behaviour(self.GetEvent())
        self.add_behaviour(self.GetAmbulanceGPS())
        self.add_behaviour(self.PrintData())