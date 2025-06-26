from pydantic import BaseModel
from typing import List, Dict

# used in Country class
class CountryName(BaseModel):
    common: str

# used in Country class
class Flag(BaseModel):
    png: str

# general country information
class Country(BaseModel):
    name: CountryName
    continents: List[str]
    population: int
    languages: Dict[str, str]
    borders: List[str]
    flags: Flag
    capital: List[str]
    cities: List[str]

class PopulationValue(BaseModel):
    year: int
    value: int

class Population(BaseModel):
    country: str
    mean: int
    values: List[PopulationValue]

# API status
class Status(BaseModel):
    countriesNowAPI: str
    restCountriesAPI: str
    version: str
    uptime: int