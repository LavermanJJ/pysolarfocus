"""Python client lib for Solarfocus"""
__version__ = "1.3.0"

import logging
from typing import Any, Tuple
from pymodbus.client.sync import ModbusTcpClient
from .component_factory import ComponentFactory

from .const import (
    Systems,
    SLAVE_ID,
    SMART_GRID_EINSCHALTUNG,
    SMART_GRID_NORMALBETRIEB,
)

from .components.base.component import Component
from .components.base.enums import DataTypes, RegisterTypes


class SolarfocusAPI:
    """Solarfocus Heating System"""

    @property
    def hc1_supply_temp(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self.heating_circuit.supply_temperature.scaled_value

    @property
    def hc1_room_temp(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self._heating_circuit_input_regs.get("HC_1_ROOM_TEMPERATURE")["value"]

    @property
    def hc1_humidity(self) -> int:
        """Supply temperature of heating circuit 1"""
        return int(self._heating_circuit_input_regs.get("HC_1_HUMIDITY")["value"])

    @property
    def hc1_limit_thermostat(self) -> int:
        """Supply temperature of heating circuit 1"""
        return int(self._heating_circuit_input_regs.get("HC_1_LIMIT_THERMOSTAT")["value"])

    @property
    def hc1_circulator_pump(self) -> int:
        """Supply temperature of heating circuit 1"""
        return int(self._heating_circuit_input_regs.get("HC_1_CIRCULATOR_PUMP")["value"])

    @property
    def hc1_mixer_valve(self) -> int:
        """Supply temperature of heating circuit 1"""
        return int(self._heating_circuit_input_regs.get("HC_1_MIXER_VALVE")["value"])

    @property
    def hc1_state(self) -> int:
        """Supply temperature of heating circuit 1"""
        return int(self._heating_circuit_input_regs.get('HC_1_STATE')['value'])
        #return HEATING_STATE.get(value, "UNKOWN")

    @property
    def bu1_top_temp(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self._buffer_input_regs.get("BU_1_TOP_TEMPERATURE")["value"]

    @property
    def bu1_bottom_temp(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self._buffer_input_regs.get("BU_1_BOTTOM_TEMPERATURE")["value"]

    @property
    def bu1_pump(self) -> int:
        """Supply temperature of heating circuit 1"""
        return self._buffer_input_regs.get("BU_1_PUMP")["value"]

    @property
    def bu1_state(self) -> int:
        """Supply temperature of heating circuit 1"""
        return int(self._buffer_input_regs.get("BU_1_STATE")["value"])
        # return BUFFER_STATE.get(value, "UNKOWN")

    @property
    def bu1_mode(self) -> int:
        """Supply temperature of heating circuit 1"""
        return int(self._buffer_input_regs.get("BU_1_MODE")["value"])
        # return BUFFER_MODE.get(value, "UNKOWN")

    @property
    def bo1_temp(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self._boiler_input_regs.get("BO_1_TEMPERATURE")["value"]

    @property
    def bo1_state(self) -> int:
        """Supply temperature of heating circuit 1"""
        return int(self._boiler_input_regs.get("BO_1_STATE")["value"])
        # return BOILER_STATE.get(value, "UNKOWN")

    @property
    def bo1_mode(self) -> int:
        """Supply temperature of heating circuit 1"""
        return int(self._boiler_input_regs.get("BO_1_MODE")["value"])
        # return BOILER_MODE.get(value, "UNKOWN")

    @property
    def hp_supply_temp(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get("SUPPLY_TEMPERATURE")["value"]

    @property
    def hp_return_temp(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get("RETURN_TEMPERATURE")["value"]

    @property
    def hp_flow_rate(self) -> int:
        """Supply temperature of heating circuit 1"""
        return int(self._heatpump_input_regs.get("FLOW_RATE")["value"])

    @property
    def hp_compressor_speed(self) -> int:
        """Supply temperature of heating circuit 1"""
        return int(self._heatpump_input_regs.get("COMPRESSOR_SPEED")["value"])

    @property
    def hp_evu_lock_active(self) -> int:
        """Supply temperature of heating circuit 1"""
        return int(self._heatpump_input_regs.get("EVU_LOCK_ACTIVE")["value"])
        # return EVU_LOCK.get(value, "UNKNOWN")

    @property
    def hp_defrost_active(self) -> int:
        """Supply temperature of heating circuit 1"""
        return int(self._heatpump_input_regs.get("DEFROST_ACTIVE")["value"])
        # return DEFROST.get(value, "UNKNOWN")

    @property
    def hp_boiler_charge(self) -> int:
        """Supply temperature of heating circuit 1"""
        return int(self._heatpump_input_regs.get("BOILER_CHARGE")["value"])
        # return BOILER_CHARGE.get(value, "UNKNOWN")

    @property
    def hp_thermal_energy_total(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get("THERMAL_ENERGY_TOTAL")["value"]

    @property
    def hp_thermal_energy_drinking_water(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get("THERMAL_ENERGY_DRINKING_WATER")["value"]

    @property
    def hp_thermal_energy_heating(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get("THERMAL_ENERGY_HEATING")["value"]

    @property
    def hp_electrical_energy_total(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get("ELECTRICAL_ENERGY_TOTAL")["value"]

    @property
    def hp_electrical_energy_drinking_water(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get("ELECTRICAL_ENERGY_DRINKING_WATER")[
            "value"
        ]

    @property
    def hp_eletrical_energy_heating(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get("ELECTRICAL_ENERGY_HEATING")["value"]

    @property
    def hp_electrical_power(self) -> int:
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get("ELECTRICAL_POWER")["value"]

    @property
    def hp_thermal_power_cooling(self) -> int:
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get("THERMAL_POWER_COOLING")["value"]

    @property
    def hp_thermal_power_heating(self) -> int:
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get("THERMAL_POWER_HEATING")["value"]

    @property
    def hp_thermal_energy_cooling(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get("THERMAL_ENERGY_COOLING")["value"]

    @property
    def hp_electrical_energy_cooling(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get("ELECTRICAL_ENERGY_COOLING")["value"]

    @property
    def hp_cop(self) -> float:
        """Supply temperature of heating circuit 1"""
        if self.hp_electrical_power:
            return self.hp_thermal_power_heating / self.hp_electrical_power
        return 0.0

    @property
    def hp_vampair_state(self) -> int:
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get("VAMPAIR_STATE")["value"]
        # return VAMPAIR_STATE.get(value, "UNKOWN")

    @property
    def pv_power(self) -> int:
        """Supply temperature of heating circuit 1"""
        return self._photovoltaic_input_regs.get("PV_POWER")["value"]

    @property
    def pv_house_consumption(self) -> int:
        """Supply temperature of heating circuit 1"""
        return self._photovoltaic_input_regs.get("HOUSE_CONSUMPTION")["value"]

    @property
    def pv_heatpump_consumption(self) -> int:
        """Supply temperature of heating circuit 1"""
        return self._photovoltaic_input_regs.get("HEATPUMP_CONSUMPTION")["value"]

    @property
    def pv_grid_import(self) -> int:
        """Supply temperature of heating circuit 1"""
        return self._photovoltaic_input_regs.get("GRID_IMPORT")["value"]

    @property
    def pv_grid_export(self) -> int:
        """Supply temperature of heating circuit 1"""
        return self._photovoltaic_input_regs.get("GRID_EXPORT")["value"]

    @property
    def hc1_target_temperatur(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self._heating_circuit_holding_regs.get("TARGET_SUPPLY_TEMPERATURE")[
            "value"
        ]

    @property
    def hc1_cooling(self) -> int:
        """Supply temperature of heating circuit 1"""
        return int(self._heating_circuit_holding_regs.get("COOLING")["value"])

    @property
    def hc1_mode_holding(self) -> int:
        """Supply temperature of heating circuit 1"""
        return int(self._heating_circuit_holding_regs.get("MODE")["value"])

    @property
    def hc1_target_room_temperatur(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self._heating_circuit_holding_regs.get("TARGET_ROOM_TEMPERATURE")[
            "value"
        ]

    @property
    def hc1_indoor_temperature_external(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self._heating_circuit_holding_regs.get("INDOOR_TEMPERATURE_EXTERNAL")[
            "value"
        ]

    @property
    def hc1_indoor_humidity_external(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self._heating_circuit_holding_regs.get("INDOOR_HUMIDITY_EXTERNAL")[
            "value"
        ]

    @property
    def bo1_target_temperatur(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self._boiler_holding_regs.get("TARGET_TEMPERATURE")["value"]

    @property
    def bo1_single_charge(self) -> int:
        """Supply temperature of heating circuit 1"""
        return int(self._boiler_holding_regs.get("SINGLE_CHARGE")["value"])

    @property
    def bo1_mode_holding(self) -> int:
        """Supply temperature of heating circuit 1"""
        return int(self._boiler_holding_regs.get("MODE")["value"])

    @property
    def bo1_ciruclation(self) -> int:
        """Supply temperature of heating circuit 1"""
        return int(self._boiler_holding_regs.get("CIRCULATION")["value"])

    @property
    def hp_evu_lock(self) -> int:
        """Supply temperature of heating circuit 1"""
        return int(self._heatpump_holding_regs.get("EVU_LOCK")["value"])

    @property
    def hp_smart_grid(self) -> int:
        """Supply temperature of heating circuit 1"""
        return int(self._heatpump_holding_regs.get("SMART_GRID")["value"])

    @property
    def hp_outdoor_temperature_external(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self._heatpump_holding_regs.get("OUTDOOR_TEMPERATURE_EXTERNAL")["value"]

    @property
    def pv_smart_meter(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self._photovoltaic_holidng_regs.get("SMART_METER")["value"]

    @property
    def pv_photovoltaic(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self._photovoltaic_holidng_regs.get("PHOTOVOLTAIC")["value"]

    @property
    def pv_grid_import_export(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self._photovoltaic_holidng_regs.get("GRID_IN_EXPORT")["value"]

    @property
    def pb_temperature(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self._pelletsboiler_input_regs.get("PELLETSBOILER_TEMPERATURE")["value"]

    @property
    def pb_status(self) -> int:
        """Supply temperature of heating circuit 1"""
        return self._pelletsboiler_input_regs.get("STATUS")["value"]

    @property
    def pb_message_number(self) -> int:
        """Supply temperature of heating circuit 1"""
        return self._pelletsboiler_input_regs.get("MESSAGE_NUMBER")["value"]

    @property
    def pb_door_contact(self) -> int:
        """Supply temperature of heating circuit 1"""
        return self._pelletsboiler_input_regs.get("DOOR_CONTACT")["value"]

    @property
    def pb_cleaning(self) -> int:
        """Supply temperature of heating circuit 1"""
        return self._pelletsboiler_input_regs.get("CLEANING")["value"]

    @property
    def pb_ash_container(self) -> int:
        """Supply temperature of heating circuit 1"""
        return self._pelletsboiler_input_regs.get("ASH_CONTAINER")["value"]

    @property
    def pb_outdoor_temperature(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self._pelletsboiler_input_regs.get("OUTDOOR_TEMPERATURE")["value"]

    @property
    def pb_octoplus_buffer_temperature_bottom(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self._pelletsboiler_input_regs.get("OCTOPLUS_BUFFER_TEMPERATURE_BOTTOM")["value"]

    @property
    def pb_octoplus_buffer_temperature_top(self) -> float:
        """Supply temperature of heating circuit 1"""
        return  self.pelletsboiler.octoplus_buffer_temperature_top.scaled_value

    @property
    def pb_log_wood_therminator(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self.pelletsboiler.log_wood.scaled_value


    def __init__(self, conn:ModbusTcpClient,system:Systems=Systems.Vampair,slave_id:int=SLAVE_ID):
        """Initialize Solarfocus communication."""
        self._conn = conn
        self.heating_circuit = ComponentFactory.heating_circuit(system)
        self.boiler = ComponentFactory.boiler(system)
        self.heatpump = ComponentFactory.heatpump(system)
        self.photovoltaic = ComponentFactory.photovoltaic(system)
        self.pelletsboiler = ComponentFactory.pelletsboiler(system)
        self.buffer = ComponentFactory.buffer(system)
        self._slave_id = slave_id

    def connect(self):
        """Connect to Solarfocus eco manager-touch"""
        return self._conn.connect()

    @property
    def is_connected(self)->bool:
        """Check if connection is established"""
        return self._conn.is_socket_open()
    
    def update(self):
        """Read values from Heating System"""
        if (
            self.update_heating()
            and self.update_buffer()
            and self.update_boiler()
            and self.update_heatpump()
            and self.update_photovoltaic()
            and self.update_pelletsboiler()
        ):
            return True
        return False

    def __update(self,component:Component)->bool:
        """Read values for the given component from Heating System"""
        failed=False
        if component.has_input_address:
            read_success, registers = self.__read_input_registers(component.input_address, component.input_count)
            parsing_success = False
            if read_success:
                parsing_success = component.parse(registers, RegisterTypes.Input) and read_success
            failed = not parsing_success and read_success or failed
             
        if component.has_holding_address:
            read_success, registers = self.__read_holding_registers(component.holding_address, component.holding_count)
            parsing_success = False
            if read_success:
                parsing_success = component.parse(registers, RegisterTypes.Holding) and read_success
            failed = not (parsing_success and read_success) or failed
        return not failed
    
    def update_heating(self) -> bool:
        """Read values from Heating System"""
        return self.__update(self.heating_circuit)
    
    def update_buffer(self) -> bool:
        """Read values from Heating System"""
        return self.__update(self.buffer)
    
    def update_boiler(self) -> bool:
        """Read values from Heating System"""
        return self.__update(self.boiler)

    def update_heatpump(self) -> bool:
        """Read values from Heating System"""
        return self.__update(self.heatpump)

    def update_photovoltaic(self) -> bool:
        """Read values from Heating System"""
        return self.__update(self.photovoltaic)

    def update_pelletsboiler(self) -> bool:
        """Read values from Pellets boiler"""
        return self.__update(self.pelletsboiler)

    def hc1_set_target_supply_temperature(self, temperature) -> bool:
        """Set target supply temperature"""
        temp_scaled = int(
            temperature * HC_REGMAP_HOLDING["TARGET_SUPPLY_TEMPERATURE"]["multiplier"]
        )
        return self.__write_registers(HC_REGMAP_HOLDING["TARGET_SUPPLY_TEMPERATURE"]["addr"],temp_scaled)


    def hc1_enable_cooling(self, cooling: bool) -> bool:
        """Set target supply temperature"""
        return self.__write_registers( HC_REGMAP_HOLDING["COOLING"]["addr"],int(cooling))
    
    def hc1_set_mode(self, mode: int) -> bool:
        """Set mode"""
        return self.__write_registers(HC_REGMAP_HOLDING["MODE"]["addr"],mode)

    def hc1_set_target_room_temperature(self, temperature: float) -> bool:
        """Set target room temperature"""
        temp_scaled = int(
            temperature * HC_REGMAP_HOLDING["TARGET_ROOM_TEMPERATURE"]["multiplier"]
        )
        return self.__write_registers(HC_REGMAP_HOLDING["TARGET_ROOM_TEMPERATURE"]["addr"],temp_scaled)
    
    def hc1_set_indoor_temperature(self, temperature: float) -> bool:
        """Set indoor temperature"""
        temp_scaled = int(
            temperature * HC_REGMAP_HOLDING["INDOOR_TEMPERATURE_EXTERNAL"]["multiplier"]
        )
        return self.__write_registers(HC_REGMAP_HOLDING["INDOOR_TEMPERATURE_EXTERNAL"]["addr"],temp_scaled)


    def hc1_set_indoor_humidity(self, humidity: float) -> bool:
        """Set indoor humidity"""
        return self.__write_registers(HC_REGMAP_HOLDING["INDOOR_HUMIDITY_EXTERNAL"]["addr"],int(humidity))
    
    def bo1_set_target_temperature(self, temperature: float) -> bool:
        """Set target temperature"""
        temp_scaled = int(
            temperature * BO_REGMAP_HOLDING["TARGET_TEMPERATURE"]["multiplier"]
        )
        return self.__write_registers(BO_REGMAP_HOLDING["TARGET_TEMPERATURE"]["addr"],temp_scaled)
    
    def bo1_enable_single_charge(self, enable: bool) -> bool:
        """Enable single charge"""
        return self.__write_registers(BO_REGMAP_HOLDING["SINGLE_CHARGE"]["addr"],int(enable))
    
    def bo1_set_mode(self, mode: int) -> bool:
        """Set mode"""
        return self.__write_registers(BO_REGMAP_HOLDING["MODE"]["addr"],mode)
    
    def bo1_enable_circulation(self, enable: bool) -> bool:
        """Enable circulation"""
        return self.__write_registers(BO_REGMAP_HOLDING["CIRCULATION"]["addr"],int(enable))


    def hp_smart_grid_request_operation(self, operation_request: bool) -> bool:
        """Set Smart Grid value"""
        return self.__write_registers(HP_REGMAP_HOLDING["SMART_GRID"]["addr"], SMART_GRID_EINSCHALTUNG if operation_request else SMART_GRID_NORMALBETRIEB)


    def hp_set_outdoor_temperature(self, temperature: float) -> bool:
        """Set outdoor temperature"""
        temp_scaled = int(
            temperature
            * HP_REGMAP_HOLDING["OUTDOOR_TEMPERATURE_EXTERNAL"]["multiplier"]
        )
        return self.__write_registers(HP_REGMAP_HOLDING["OUTDOOR_TEMPERATURE_EXTERNAL"]["addr"],temp_scaled)
    
    def pv_set_smart_meter(self, value: int) -> bool:
        """Set Smart Meter"""
        return self.__write_registers(PV_REGMAP_HOLDING["SMART_METER"]["addr"],value)

    def pv_set_photovoltaic(self, value: int) -> bool:
        """Set Photovoltaic"""
        return self.__write_registers(PV_REGMAP_HOLDING["PHOTOVOLTAIC"]["addr"], value)


    def pv_set_grid_im_export(self, value: int) -> bool:
        """Set Photovoltaic"""
        return self.__write_registers(PV_REGMAP_HOLDING["GRID_IM_EXPORT"]["addr"],value)


    def __write_registers(self,address:int, value:int, check_connection:bool = True) -> bool:
        """Internal methode to write registers to the modbus server"""
        if check_connection and not self.is_connected:
            logging.error("Connection to modbus is not established!")
            return False
        try:
            response = self._conn.write_registers(address, [value], unit=self._slave_id)
            if response.isError():
                logging.error(f"Error writing value={value} to register: {address}: {response}")
                return False
        except Exception:
            logging.exception(f"Eception while writing value={value} to register: {address}!")
            return False
        return True

    def __read_holding_registers(self,address:int, count:int, check_connection:bool = True)->Tuple[bool,Any]:
        """Internal methode to read holding registers from modbus"""
        if check_connection and not self.is_connected:
            logging.error("Connection to modbus is not established!")
            return False, None
        try:
            result = self._conn.read_holding_registers(address=address,count=count ,unit=self._slave_id)
            if result.isError():
                logging.error(f"Modbus read error at address={address}: {result}")
                return False, None
            return True, result.registers
        except Exception:
            logging.exception(f"Exception while reading holding registers at address={address}!")
            return False, None
        
    def __read_input_registers(self,address:int,count:int,check_connection:bool=True)->Tuple[bool,Any]:
        """Internal methode to read input registers from modbus"""
        if check_connection and not self.is_connected:
            logging.error("Connection to modbus is not established!")
            return False, None
        try:
            result = self._conn.read_input_registers(address=address, count=count,unit=self._slave_id)
            if result.isError():
                logging.error(f"Modbus read error at address={address}, count={count}: {result}")
                return False, None
            return True, result.registers
        except Exception:
            logging.exception(f"Exception while reading input registers at address={address}, count={count}!")
            return False, None
