"""Python client lib for Solarfocus"""
__version__ = "2.0.4"

import logging
from enum import Enum

from pymodbus.client.sync import ModbusTcpClient

#Default port for modbus
PORT = 502

#This needs to be defined before the imports because of circular dependencies
class Systems(str, Enum):
    """
    Supported systems by this library
    """
    Vampair = "Vampair"
    Therminator = "Therminator" 
    
from .component_factory import ComponentFactory
from .components.base.component import Component
from .components.base.data_value import DataValue
from .components.base.enums import RegisterTypes
from .const import SLAVE_ID, SMART_GRID_EINSCHALTUNG, SMART_GRID_NORMALBETRIEB

class SolarfocusAPI:
    """Solarfocus Heating System"""

    @property
    def hc1_supply_temp(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self.heating_circuit.supply_temperature.scaled_value

    @property
    def hc1_room_temp(self) -> float:
        """room temperature of heating circuit 1"""
        return self.heating_circuit.room_temperature.scaled_value

    @property
    def hc1_humidity(self) -> int:
        """humidity of heating circuit 1"""
        return int(self.heating_circuit.humidity.scaled_value)
    @property
    def hc1_limit_thermostat(self) -> int:
        """limit temperature of heating circuit 1"""
        return int(self.heating_circuit.limit_temperature.scaled_value)
    @property
    def hc1_circulator_pump(self) -> int:
        """circulator pump of heating circuit 1"""
        return int(self.heating_circuit.circulator_pump.scaled_value)

    @property
    def hc1_mixer_valve(self) -> int:
        """mixer valve of heating circuit 1"""
        return int(self.heating_circuit.mixer_valve.scaled_value)

    @property
    def hc1_state(self) -> int:
        """state of heating circuit 1"""
        return int(self.heating_circuit.state.scaled_value)

    @property
    def hc1_target_temperatur(self) -> float:
        return self.heating_circuit.target_supply_temperature.reverse_scaled_value

    @property
    def hc1_cooling(self) -> int:
        return int(self.heating_circuit.cooling.scaled_value)

    @property
    def hc1_mode_holding(self) -> int:
        return int(self.heating_circuit.mode.scaled_value)

    @property
    def hc1_target_room_temperatur(self) -> float:
        return self.heating_circuit.target_room_temperatur.reverse_scaled_value

    @property
    def hc1_indoor_temperature_external(self) -> float:
        return self.heating_circuit.indoor_temperatur_external.scaled_value

    @property
    def hc1_indoor_humidity_external(self) -> float:
        return self.heating_circuit.indoor_humidity_external.scaled_value
    
    @property
    def bu1_top_temp(self) -> float:
        return self.buffer.top_temperature.scaled_value

    @property
    def bu1_bottom_temp(self) -> float:
        return self.buffer.bottom_temperature.scaled_value

    @property
    def bu1_pump(self) -> int:
        return int(self.buffer.pump.scaled_value)

    @property
    def bu1_state(self) -> int:
        return int(self.buffer.state.scaled_value)
    
    @property
    def bu1_mode(self) -> int:
        return int(self.buffer.mode.scaled_value)

    @property
    def bo1_temp(self) -> float:
        return self.boiler.temperature.scaled_value

    @property
    def bo1_state(self) -> int:
        return int(self.boiler.state.scaled_value)

    @property
    def bo1_mode(self) -> int:
        return int(self.boiler.mode.scaled_value)

    @property
    def bo1_target_temperatur(self) -> float:
        return self.boiler.target_temperature.reverse_scaled_value

    @property
    def bo1_single_charge(self) -> int:
        return self.boiler.single_charge.scaled_value

    @property
    def bo1_mode_holding(self) -> int:
        return self.boiler.holding_mode.scaled_value #dont know if this is needed

    @property
    def bo1_ciruclation(self) -> int:
        return self.boiler.circulation.scaled_value
    
    @property
    def hp_supply_temp(self) -> float:
        return self.heatpump.supply_temperature.scaled_value
    @property
    def hp_return_temp(self) -> float:
        return self.heatpump.return_temperatur.scaled_value

    @property
    def hp_flow_rate(self) -> int:
        return int(self.heatpump.flow_rate.scaled_value)

    @property
    def hp_compressor_speed(self) -> int:
        return int(self.heatpump.compressor_speed.scaled_value)

    @property
    def hp_evu_lock_active(self) -> int:
        return int(self.heatpump.evu_lock_active.scaled_value)

    @property
    def hp_defrost_active(self) -> int:
        return int(self.heatpump.defrost_active.scaled_value)

    @property
    def hp_boiler_charge(self) -> int:
        return int(self.heatpump.boilder_charge.scaled_value)

    @property
    def hp_thermal_energy_total(self) -> float:
        return self.heatpump.thermal_energy_total.scaled_value

    @property
    def hp_thermal_energy_drinking_water(self) -> float:
        return self.heatpump.thermal_energy_drinking_water.scaled_value

    @property
    def hp_thermal_energy_heating(self) -> float:
        return self.heatpump.thermal_energy_heating.scaled_value

    @property
    def hp_electrical_energy_total(self) -> float:
        return self.heatpump.electrical_energy_total.scaled_value

    @property
    def hp_electrical_energy_drinking_water(self) -> float:
        return self.heatpump.electrical_energy_drinking_water.scaled_value

    @property
    def hp_eletrical_energy_heating(self) -> float:
        return self.heatpump.electrical_energy_heating.scaled_value

    @property
    def hp_electrical_power(self) -> int:
        return self.heatpump.electrical_power.scaled_value

    @property
    def hp_thermal_power_cooling(self) -> int:
        return self.heatpump.thermal_power_cooling.scaled_value

    @property
    def hp_thermal_power_heating(self) -> int:
        return self.heatpump.thermal_power_heating.scaled_value

    @property
    def hp_thermal_energy_cooling(self) -> float:
        return self.heatpump.thermal_energy_cooling.scaled_value

    @property
    def hp_electrical_energy_cooling(self) -> float:
        return self.heatpump.electrical_energy_cooling.scaled_value

    @property
    def hp_cop(self) -> float:
        if self.heatpump.electrical_power.scaled_value:
            return self.heatpump.thermal_power_heating.scaled_value / self.heatpump.electrical_power.scaled_value
        return 0.0

    @property
    def hp_vampair_state(self) -> int:
        return int(self.heatpump.vampair_state.scaled_value)

    @property
    def hp_evu_lock(self) -> int:
        return int(self.heatpump.evu_lock.scaled_value)

    @property
    def hp_smart_grid(self) -> int:
        return int(self.heatpump.smart_grid.scaled_value)

    @property
    def hp_outdoor_temperature_external(self) -> float:
        return self.heatpump.outdoor_temperature_external.reverse_scaled_value
    
    @property
    def pv_power(self) -> int:
        return int(self.photovoltaic.power.scaled_value)

    @property
    def pv_house_consumption(self) -> int:
        return int(self.photovoltaic.house_consumption.scaled_value)

    @property
    def pv_heatpump_consumption(self) -> int:
        return int(self.photovoltaic.heatpump_consumption.scaled_value)

    @property
    def pv_grid_import(self) -> int:
        return int(self.photovoltaic.grid_import.scaled_value)

    @property
    def pv_grid_export(self) -> int:
        return int(self.photovoltaic.grid_export.scaled_value)

    @property
    def pv_smart_meter(self) -> float:
        return self.photovoltaic.smart_meter.scaled_value

    @property
    def pv_photovoltaic(self) -> float:
        return self.photovoltaic.photovoltaic.scaled_value

    @property
    def pv_grid_import_export(self) -> float:
        return self.photovoltaic.grid_im_export.scaled_value
    
    @property
    def pb_temperature(self) -> float:
        return self.pelletsboiler.temperature.scaled_value

    @property
    def pb_status(self) -> int:
        return self.pelletsboiler.status.scaled_value

    @property
    def pb_message_number(self) -> int:
        return self.pelletsboiler.message_number.scaled_value

    @property
    def pb_door_contact(self) -> int:
        return self.pelletsboiler.door_contact.scaled_value

    @property
    def pb_cleaning(self) -> int:
        return self.pelletsboiler.cleaning.scaled_value

    @property
    def pb_ash_container(self) -> int:
        return self.pelletsboiler.ash_container.scaled_value

    @property
    def pb_outdoor_temperature(self) -> float:
        return self.pelletsboiler.outdoor_temperature.scaled_value

    @property
    def pb_octoplus_buffer_temperature_bottom(self) -> float:
        return self.pelletsboiler.octoplus_buffer_temperature_bottom.scaled_value

    @property
    def pb_octoplus_buffer_temperature_top(self) -> float:
        return self.pelletsboiler.octoplus_buffer_temperature_top.scaled_value

    @property
    def pb_log_wood_therminator(self) -> float:
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
    
    def __update(self,component:Component)->bool:
        """Read values for the given component from Heating System"""
        failed=False
        if component.has_input_address:
            read_success, registers = self.__read_input_registers(component)
            parsing_success = False
            if read_success:
                parsing_success = component.parse(registers, RegisterTypes.Input) and read_success
            failed = not parsing_success and read_success or failed
             
        if component.has_holding_address:
            read_success, registers = self.__read_holding_registers(component)
            parsing_success = False
            if read_success:
                parsing_success = component.parse(registers, RegisterTypes.Holding) and read_success
            failed = not (parsing_success and read_success) or failed
        return not failed
    
    
    def hc1_set_target_supply_temperature(self, temperature) -> bool:
        """Set target supply temperature"""
        return self.__write_register(self.heating_circuit.target_supply_temperature,temperature)


    def hc1_enable_cooling(self, cooling: bool) -> bool:
        """Set target supply temperature"""
        return self.__write_register(self.heating_circuit.cooling,cooling)
    
    def hc1_set_mode(self, mode: int) -> bool:
        """Set mode"""
        return self.__write_register(self.heating_circuit.mode,mode)

    def hc1_set_target_room_temperature(self, temperature: float) -> bool:
        """Set target room temperature"""
        return self.__write_register(self.heating_circuit.target_room_temperatur,temperature)
    
    def hc1_set_indoor_temperature(self, temperature: float) -> bool:
        """Set indoor temperature"""
        return self.__write_register(self.heating_circuit.indoor_temperatur_external,temperature)
    
    def hc1_set_indoor_humidity(self, humidity: float) -> bool:
        """Set indoor humidity"""
        return self.__write_register(self.heating_circuit.indoor_humidity_external,int(humidity))
    
    def bo1_set_target_temperature(self, temperature: float) -> bool:
        """Set target temperature"""
        return self.__write_register(self.boiler.target_temperature,temperature)
    
    def bo1_enable_single_charge(self, enable: bool) -> bool:
        """Enable single charge"""
        return self.__write_register(self.boiler.single_charge,int(enable))
    
    def bo1_set_mode(self, mode: int) -> bool:
        """Set mode"""
        return self.__write_register(self.boiler.mode,mode)
    
    def bo1_enable_circulation(self, enable: bool) -> bool:
        """Enable circulation"""
        return self.__write_register(self.boiler.circulation,int(enable))

    def hp_smart_grid_request_operation(self, operation_request: bool) -> bool:
        """Set Smart Grid value"""
        return self.__write_register(self.heatpump.smart_grid, SMART_GRID_EINSCHALTUNG if operation_request else SMART_GRID_NORMALBETRIEB)

    def hp_set_outdoor_temperature(self, temperature: float) -> bool:
        """Set outdoor temperature"""
        return self.__write_register(self.heatpump.outdoor_temperature_external,temperature)
    
    def pv_set_smart_meter(self, value: int) -> bool:
        """Set Smart Meter"""
        return self.__write_register(self.photovoltaic.smart_meter,value)

    def pv_set_photovoltaic(self, value: int) -> bool:
        """Set Photovoltaic"""
        return self.__write_register(self.photovoltaic.photovoltaic, value)


    def pv_set_grid_im_export(self, value: int) -> bool:
        """Set Photovoltaic"""
        return self.__write_register(self.photovoltaic.grid_im_export,value)
    
    def __write_register(self,data_value:DataValue, value:float, check_connection:bool = True) -> bool:
        """Internal methode to write a value to the modbus server"""
        if check_connection and not self.is_connected:
            logging.error("Connection to modbus is not established!")
            return False
        try:
            scaled = int(data_value.scale(value))
            logging.info(f"Scaled Value={scaled}")
            response = self._conn.write_registers(data_value.get_absolute_address(), [scaled], unit=self._slave_id)
            if response.isError():
                logging.error(f"Error writing value={value} to register: {data_value.get_absolute_address()}: {response}")
                return False
        except Exception:
            logging.exception(f"Eception while writing value={value} to register: {data_value.get_absolute_address()}!")
            return False
        return True

    def __read_holding_registers(self,component:Component, check_connection:bool = True)->tuple[bool,list[int]]:
        """Internal methode to read holding registers from modbus"""
        if check_connection and not self.is_connected:
            logging.error("Connection to modbus is not established!")
            return False, None
        try:
            combined_result = [None] * component.holding_count
            for registerSlice in component.holding_slices:
                result = self._conn.read_holding_registers(address=registerSlice.absolute_address,count=registerSlice.count ,unit=self._slave_id)
                if result.isError():
                    logging.error(f"Modbus read error at address={registerSlice.absolute_address}: {result}")
                    return False, None
                slice_data = result.registers
                combined_result[registerSlice.relative_address:registerSlice.relative_address+registerSlice.count] = slice_data
            return True, combined_result
        except Exception:
            logging.exception(f"Exception while reading holding registers for component: '{component.__class__.__name__}'!")
            return False, None
        
    def __read_input_registers(self,component:Component,check_connection:bool=True)->tuple[bool,list[int]]:
        """Internal methode to read input registers from modbus"""
        if check_connection and not self.is_connected:
            logging.error("Connection to modbus is not established!")
            return False, None
        try:
            combined_result = [None] * component.input_count
            for registerSlice in component.input_slices:
                result = self._conn.read_input_registers(address=registerSlice.absolute_address,count=registerSlice.count,unit=self._slave_id)
                if result.isError():
                    logging.error(f"Modbus read error at address={registerSlice.absolute_address}, count={registerSlice.count}: {result}")
                    return False, None
                slice_data = result.registers
                combined_result[registerSlice.relative_address:registerSlice.relative_address+registerSlice.count] = slice_data
            return True, combined_result
        except Exception:
            logging.exception(f"Exception while reading input registers for component: '{component.__class__.__name__}'!")
            return False, None
