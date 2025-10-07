from typing import List

from .schemas import Payload, PowerPlant
from .optimizer import WindTurbine, ThermalPlant


def parse_powerplants(powerplants: List[PowerPlant]):
    wind_turbines: List[WindTurbine] = []
    thermal_plants: List[ThermalPlant] = []
    for p in powerplants:
        if p.type == "windturbine":
            wt = WindTurbine(p.name, p.pmax)
            wind_turbines.append(wt)
        else:
            tp = ThermalPlant(p.name, p.type, p.efficiency, p.pmin, p.pmax)
            thermal_plants.append(tp)
    return wind_turbines, thermal_plants


def parse_payload(payload: Payload):
    wind_turbines, thermal_plants = parse_powerplants(payload.powerplants)
    return payload.load, payload.fuels, wind_turbines, thermal_plants
