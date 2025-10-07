from itertools import combinations
from typing import List, Tuple, Literal, Optional, cast

from .schemas import Fuels


class InsufficientCapacityError(Exception):
    """Raised when the available power plants cannot meet the required load."""
    pass


class WindTurbine:
    def __init__(self, name: str, pmax: float):
        self.name = name
        self.pmax = pmax
        self.p: Optional[float] = None

    def set_real_power(self, wind_percent: float) -> None:
        self.p = self.pmax * wind_percent / 100


class ThermalPlant:
    def __init__(self, name: str, plant_type: Literal["gasfired", "turbojet"], efficiency: float, pmin: float, pmax: float):
        self.name = name
        self.plant_type = plant_type
        self.pmin = pmin
        self.pmax = pmax
        self.p = 0.0
        self.efficiency = efficiency
        self.cost_per_mwh: Optional[float] = None

    def set_cost(self, fuel_price: float) -> None:
        self.cost_per_mwh = fuel_price / self.efficiency


class PowerPlantOptimizer:
    """
    Optimizes the power output of a set of wind turbines and thermal plants to meet a given load
    at minimum cost, considering plant constraints and fuel prices.

    Attributes:
        load (float): The required total power output.
        fuels (Fuels): Fuel prices and wind percentage information.
        wind_turbines (List[WindTurbine]): List of available wind turbines.
        thermal_plants (List[ThermalPlant]): List of available thermal plants.
    """

    def __init__(self, load: float, fuels: Fuels, wind_turbines: List[WindTurbine], thermal_plants: List[ThermalPlant]):
        self.load = load
        self.fuels = fuels
        self.wind_turbines: List[WindTurbine] = wind_turbines
        self.thermal_plants: List[ThermalPlant] = thermal_plants

    def wind_optimizer(self, wind_turbines: List[WindTurbine], load: float) -> Tuple[List[WindTurbine], float]:
        """
        Selects the optimal combination of wind turbines to meet the load as closely as possible without exceeding it.
        The current implementation uses a brute-force approach to evaluate all combinations of wind turbines.
        """
        for wt in wind_turbines:
            wt.set_real_power(self.fuels.wind_percent)

        total_wind_power = sum(wt.p for wt in wind_turbines if wt.p is not None)
        if total_wind_power <= self.load:
            return wind_turbines, total_wind_power

        best_combination: List[WindTurbine] = []
        best_power = 0.0

        for r in range(1, len(wind_turbines) + 1):
            for combo in combinations(wind_turbines, r):
                total_power = sum(wt.p for wt in combo if wt.p is not None)
                if total_power <= load and total_power > best_power:
                    best_combination = list(combo)
                    best_power = total_power
        return best_combination, best_power

    def thermal_optimizer(self, thermal_plants: List[ThermalPlant], remaining_load: float) -> List[ThermalPlant]:
        """
        Optimizes the power output of thermal plants to cover the remaining load after wind power has been accounted for.
        Plants are sorted by cost efficiency, and power is allocated to minimize costs while respecting
        their minimum and maximum power constraints.
        """
        for tp in thermal_plants:
            if tp.plant_type == "gasfired":
                tp.set_cost(self.fuels.gas_euro_per_mwh)
            elif tp.plant_type == "turbojet":
                tp.set_cost(self.fuels.kerosine_euro_per_mwh)

        thermal_plants.sort(key=lambda x: cast(float, x.cost_per_mwh))
        for tp in thermal_plants:
            if remaining_load <= 0:
                continue
            if tp.pmin > remaining_load:
                tp.p = 0.0
            elif tp.pmax <= remaining_load:
                tp.p = tp.pmax
            elif tp.pmin <= remaining_load < tp.pmax:
                tp.p = remaining_load
            remaining_load -= tp.p
        if remaining_load > 0:
            raise InsufficientCapacityError
        return thermal_plants

    def optimize(self) -> List[ThermalPlant | WindTurbine]:

        used_plants = []

        # Select optimal wind turbines
        selected_wind, wind_power = self.wind_optimizer(self.wind_turbines, self.load)
        for wt in self.wind_turbines:
            wt.p = wt.p if wt in selected_wind else 0.0
        used_plants += self.wind_turbines
        remaining_load = self.load - wind_power

        # Optimize thermal plants to cover remaining load
        selected_thermal = self.thermal_optimizer(self.thermal_plants, remaining_load)
        used_plants += selected_thermal

        return used_plants
