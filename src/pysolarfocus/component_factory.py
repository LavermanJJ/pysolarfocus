"""Solarfocus component factory"""
from . import ApiVersions, Systems
from .components.biomass_boiler import BiomassBoiler
from .components.boiler import Boiler
from .components.buffer import Buffer, TherminatorBuffer
from .components.circulation import Circulation
from .components.differential_module import DifferentialModule
from .components.fresh_water_module import FreshWaterModule
from .components.heat_pump import HeatPump
from .components.heating_circuit import HeatingCircuit, TherminatorHeatingCircuit
from .components.photovoltaic import Photovoltaic
from .components.solar import Solar
from .modbus_wrapper import ModbusConnector


class ComponentFactory:
    def __init__(self, modbus_connector: ModbusConnector) -> None:
        self.__modbus_connector = modbus_connector

    def heating_circuit(self, system: Systems, count: int, api_version: ApiVersions) -> list[HeatingCircuit]:
        input_addresses = list(range(1100, 1100 + (50 * count), 50))
        holding_addresses = list(range(32600, 32600 + (50 * count), 50))
        heating_circuits = []
        for i in range(count):
            input, holding = input_addresses[i], holding_addresses[i]
            if system in [Systems.THERMINATOR, Systems.ECOTOP]:
                heating_circuit = TherminatorHeatingCircuit(input, holding, api_version=api_version).initialize(self.__modbus_connector)
            else:
                heating_circuit = HeatingCircuit(input, holding, api_version=api_version).initialize(self.__modbus_connector)
            heating_circuits.append(heating_circuit)
        return heating_circuits

    def boiler(self, system: Systems, count: int, api_version: ApiVersions) -> list[Boiler]:
        input_addresses = list(range(500, 500 + (50 * count), 50))
        holding_addresses = list(range(32000, 32000 + (50 * count), 50))
        boilers = []
        for i in range(count):
            input, holding = input_addresses[i], holding_addresses[i]
            boilers.append(Boiler(input, holding, api_version=api_version).initialize(self.__modbus_connector))
        return boilers

    def buffer(self, system: Systems, count: int, api_version: ApiVersions) -> list[Buffer]:
        input_addresses = list(range(1900, 1900 + (20 * count), 20))
        holding_addresses = -1
        if api_version.greater_or_equal(ApiVersions.V_22_090.value):
            holding_addresses = list(range(34000, 34000 + (50 * count), 50))
        buffers = []
        for i in range(count):
            input = input_addresses[i]
            if api_version.greater_or_equal(ApiVersions.V_22_090.value):
                holding = holding_addresses[i]
            else:
                holding = -1
            if system in [Systems.THERMINATOR, Systems.ECOTOP]:
                buffer = TherminatorBuffer(input).initialize(self.__modbus_connector)
            else:
                buffer = Buffer(input, holding, api_version=api_version).initialize(self.__modbus_connector)
            buffers.append(buffer)
        return buffers

    def fresh_water_modules(self, system: Systems, count: int, api_version: ApiVersions) -> list[FreshWaterModule]:
        input_addresses = list(range(700, 700 + (25 * count), 25))
        fresh_water_modules = []
        for i in range(count):
            input = input_addresses[i]
            fresh_water_modules.append(FreshWaterModule(input, api_version=api_version).initialize(self.__modbus_connector))
        return fresh_water_modules

    def circulation(self, system: Systems, count: int, api_version: ApiVersions) -> list[Circulation]:
        input_addresses = list(range(900, 900 + (25 * count), 25))
        circulation = []
        for i in range(count):
            input = input_addresses[i]
            circulation.append(Circulation(input, api_version=api_version).initialize(self.__modbus_connector))
        return circulation

    def differential_modules(self, system: Systems, count: int, api_version: ApiVersions) -> list[DifferentialModule]:
        input_addresses = list(range(2200, 2200 + (10 * count), 10))
        differential_modules = []
        for i in range(count):
            input = input_addresses[i]
            differential_modules.append(DifferentialModule(input, api_version=api_version).initialize(self.__modbus_connector))
        return differential_modules

    def heatpump(self, system: Systems, api_version: ApiVersions) -> HeatPump:
        return HeatPump(api_version=api_version).initialize(self.__modbus_connector)

    def photovoltaic(self, system: Systems, api_version: ApiVersions) -> Photovoltaic:
        return Photovoltaic(api_version=api_version).initialize(self.__modbus_connector)

    def pelletsboiler(self, system: Systems, api_version: ApiVersions) -> BiomassBoiler:
        return BiomassBoiler(api_version=api_version, system=system).initialize(self.__modbus_connector)

    def solar(self, system: Systems, count: int, api_version: ApiVersions) -> list[Solar]:
        input_addresses = list(range(2100, 2100 + (20 * count), 20))
        solar_modules = []
        for i in range(count):
            input = input_addresses[i]
            solar_modules.append(Solar(input, api_version=api_version).initialize(self.__modbus_connector))
        return solar_modules
