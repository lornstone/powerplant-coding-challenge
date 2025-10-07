from typing import List, Literal

from pydantic import BaseModel, Field


class Fuels(BaseModel):
    gas_euro_per_mwh: float = Field(alias="gas(euro/MWh)", ge=0)
    kerosine_euro_per_mwh: float = Field(alias="kerosine(euro/MWh)", ge=0)
    co2_euro_per_ton: float = Field(alias="co2(euro/ton)", ge=0)
    wind_percent: float = Field(alias="wind(%)", ge=0, le=100)


class PowerPlant(BaseModel):
    name: str
    type: Literal["gasfired", "turbojet", "windturbine"]
    efficiency: float = Field(ge=0, le=1)
    pmin: float = Field(ge=0)
    pmax: float = Field(ge=0)


class Payload(BaseModel):
    load: float = Field(ge=0)
    fuels: Fuels
    powerplants: List[PowerPlant]
