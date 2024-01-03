import spade
from agents.EmergencyCenter import EmergencyCenter
from agents.AmbulanceCoordinator import AmbulanceCoordinator
from agents.Ambulance import Ambulance
from agents.RouteCoordinator import RouteCoordinator
from agents.TrafficLightsCoordinator import TrafficLightCoordinator


async def main():

    print('\n')

    emergency_center_agent = EmergencyCenter("emergency_center@localhost", "agent")
    await emergency_center_agent.start(auto_register=True)

    ambulance_coordinator_agent = AmbulanceCoordinator("ambulance_coordinator@localhost", "agent")
    await ambulance_coordinator_agent.start(auto_register=True)

    ambulance_1_agent = Ambulance("ambulance_1@localhost", "agent", 1, [10,10])
    await ambulance_1_agent.start(auto_register=True)

    ambulance_2_agent = Ambulance("ambulance_2@localhost", "agent", 2, [11,11])
    await ambulance_2_agent.start(auto_register=True)

    route_coordinator_agent = RouteCoordinator("route_coordinator@localhost", "agent")
    await route_coordinator_agent.start(auto_register=True)

    traffic_light_coordinator = TrafficLightCoordinator("traffic_light_coordinator@localhost", "agent")
    await traffic_light_coordinator.start(auto_register=True)


if __name__ == "__main__":
    spade.run(main())
