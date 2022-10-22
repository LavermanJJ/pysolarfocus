"""Python client lib for Solarfocus"""
__version__ = "2.0.5"

import logging
from enum import Enum

#Default port for modbus
PORT = 502

#This needs to be defined before the imports because of circular dependencies
class Systems(str, Enum):
    """
    Supported systems by this library
    """
    Vampair = "Vampair"
    Therminator = "Therminator" 
    
from .modbus_wrapper import ModbusConnector
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
        return self.heating_circuit.target_supply_temperature.scaled_value

    @property
    def hc1_cooling(self) -> int:
        return int(self.heating_circuit.cooling.scaled_value)

    @property
    def hc1_mode_holding(self) -> int:
        return int(self.heating_circuit.mode.scaled_value)

    @property
    def hc1_target_room_temperatur(self) -> float:
        return self.heating_circuit.target_room_temperatur.scaled_value

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
        return self.boiler.target_temperature.scaled_value

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
        return self.heatpump.outdoor_temperature_external.scaled_value
    
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
    
    @property
    def system(self): 
        return self._system
    
    def __init__(self,
                 ip:str,
                 heating_circuit_count:int = 1,
                 buffer_count:int = 1,
                 boiler_count:int = 1,
                 system:Systems=Systems.Vampair,
                 port:int=PORT,
                 slave_id:int=SLAVE_ID):
        """Initialize Solarfocus communication."""
        assert heating_circuit_count >= 1 and heating_circuit_count < 9, "Heating circuit count must be between 1 and 8"
        assert buffer_count >= 1 and buffer_count < 5, "Buffer count must be between 1 and 4"
        assert boiler_count >= 1 and boiler_count < 5, "Boiler count must be between 1 and 4"
        
        self.__conn = ModbusConnector(ip,port,slave_id)
        self.__factory = ComponentFactory(self.__conn)
        #Lists of components
        self.heating_circuits = self.__factory.heating_circuit(system,heating_circuit_count)
        self.boilers = self.__factory.boiler(system,boiler_count)
        self.buffers = self.__factory.buffer(system,buffer_count)
        #Single components
        self.heatpump = self.__factory.heatpump(system)
        self.photovoltaic = self.__factory.photovoltaic(system)
        self.pelletsboiler = self.__factory.pelletsboiler(system)
        self._slave_id = slave_id
        self._system = system

    #These are needed to keep compatability with the old getter Api
    @property
    def heating_circuit(self):
        return self.heating_circuits[0]
    
    @property
    def boiler(self):
        return self.boilers[0]
    
    @property
    def buffer(self):
        return self.buffers[0]
    
    def connect(self):
        """Connect to Solarfocus eco manager-touch"""
        return self.__conn.connect()

    @property
    def is_connected(self)->bool:
        """Check if connection is established"""
        return self.__conn.is_connected
    
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
        for heating_circuit in self.heating_circuits:
            if not heating_circuit.update():
                return False
        return True
    
    def update_buffer(self) -> bool:
        """Read values from Heating System"""
        for buffer in self.buffers:
            if not buffer.update():
                return False
        return True
    
    def update_boiler(self) -> bool:
        """Read values from Heating System"""
        for boiler in self.boilers:
            if not boiler.update():
                return False
        return True

    def update_heatpump(self) -> bool:
        """Read values from Heating System"""
        return self.heatpump.update()

    def update_photovoltaic(self) -> bool:
        """Read values from Heating System"""
        return self.photovoltaic.update()

    def update_pelletsboiler(self) -> bool:
        """Read values from Pellets boiler"""
        return self.pelletsboiler.update()
    
    def hc1_set_target_supply_temperature(self, temperature) -> bool:
        """Set target supply temperature"""
        self.heating_circuit.target_supply_temperature.set_unscaled_value(temperature)
        return self.heating_circuit.target_supply_temperature.commit()
    
    def hc1_enable_cooling(self, cooling: bool) -> bool:
        """Set target supply temperature"""
        self.heating_circuit.cooling.set_unscaled_value(cooling)
        return self.heating_circuit.cooling.commit()
    
    def hc1_set_mode(self, mode: int) -> bool:
        """Set mode"""
        self.heating_circuit.mode.set_unscaled_value(mode)
        return self.heating_circuit.mode.commit()
    
    def hc1_set_target_room_temperature(self, temperature: float) -> bool:
        """Set target room temperature"""
        self.heating_circuit.target_room_temperatur.set_unscaled_value(temperature)
        return self.heating_circuit.target_room_temperatur.commit()
    
    def hc1_set_indoor_temperature(self, temperature: float) -> bool:
        """Set indoor temperature"""
        self.heating_circuit.indoor_temperatur_external.set_unscaled_value(temperature)
        return self.heating_circuit.indoor_temperatur_external.commit()
    
    def hc1_set_indoor_humidity(self, humidity: float) -> bool:
        """Set indoor humidity"""
        self.heating_circuit.indoor_humidity_external.set_unscaled_value(humidity)
        return self.heating_circuit.indoor_humidity_external.commit()
    
    def bo1_set_target_temperature(self, temperature: float) -> bool:
        """Set target temperature"""
        self.boiler.target_temperature.set_unscaled_value(temperature)
        return self.boiler.target_temperature.commit()
    
    def bo1_enable_single_charge(self, enable: bool) -> bool:
        """Enable single charge"""
        self.boiler.single_charge.set_unscaled_value(enable)
        return self.boiler.single_charge.commit()
    
    def bo1_set_mode(self, mode: int) -> bool:
        """Set mode"""
        self.boiler.mode.set_unscaled_value(mode)
        return self.boiler.mode.commit()
    
    def bo1_enable_circulation(self, enable: bool) -> bool:
        """Enable circulation"""
        self.boiler.circulation.set_unscaled_value(enable)
        return self.boiler.circulation.commit()

    def hp_smart_grid_request_operation(self, operation_request: bool) -> bool:
        """Set Smart Grid value"""
        self.heatpump.smart_grid.set_unscaled_value(SMART_GRID_EINSCHALTUNG if operation_request else SMART_GRID_NORMALBETRIEB)
        return self.heatpump.smart_grid.commit()

    def hp_set_outdoor_temperature(self, temperature: float) -> bool:
        """Set outdoor temperature"""
        self.heatpump.outdoor_temperature_external.set_unscaled_value(temperature)
        return self.heatpump.outdoor_temperature_external.commit()
    
    def pv_set_smart_meter(self, value: int) -> bool:
        """Set Smart Meter"""
        self.photovoltaic.smart_meter.set_unscaled_value(value)
        return self.photovoltaic.smart_meter.commit()

    def pv_set_photovoltaic(self, value: int) -> bool:
        """Set Photovoltaic"""
        self.photovoltaic.photovoltaic.set_unscaled_value(value)
        return self.photovoltaic.photovoltaic.commit()
        
    def pv_set_grid_im_export(self, value: int) -> bool:
        """Set Photovoltaic"""
        self.photovoltaic.grid_im_export.set_unscaled_value(value)
        return self.photovoltaic.grid_im_export.commit()