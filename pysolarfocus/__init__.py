__version__ = '1.0.0'


from .const import (
    BO_COUNT, 
    BO_REGMAP_INPUT, 
    BO_START_ADDR, 
    BOILER_MODE, 
    BOILER_STATE, 
    BU_COUNT, 
    BU_REGMAP_INPUT, 
    BU_START_ADDR, 
    BUFFER_MODE, 
    BUFFER_STATE, 
    HC_COUNT, 
    HC_REGMAP_INPUT, 
    HC_START_ADDR, 
    HEATING_STATE, 
    HP_COUNT, 
    HP_REGMAP_INPUT, 
    HP_START_ADDR, 
    INT, 
    PV_COUNT, 
    PV_REGMAP_INPUT, 
    PV_START_ADDR, 
    SLAVE_ID, 
    VAMPAIR_STATE
)


class SolarfocusAPI():
    """Solarfocus Heating System"""

    @property
    def hc1_supply_temp(self):
        """Supply temperature of heating circuit 1"""
        return self._heating_circuit_input_regs.get('HC_1_SUPPLY_TEMPERATURE')['value']

    @property
    def hc1_room_temp(self):
        """Supply temperature of heating circuit 1"""
        return self._heating_circuit_input_regs.get('HC_1_ROOM_TEMPERATURE')['value']

    @property
    def hc1_humidity(self):
        """Supply temperature of heating circuit 1"""
        return self._heating_circuit_input_regs.get('HC_1_HUMIDITY')['value']

    @property
    def hc1_limit_thermostat(self):
        """Supply temperature of heating circuit 1"""
        return self._heating_circuit_input_regs.get('HC_1_LIMIT_THERMOSTAT')['value']

    @property
    def hc1_circulator_pump(self):
        """Supply temperature of heating circuit 1"""
        return self._heating_circuit_input_regs.get('HC_1_CIRCULATOR_PUMP')['value']

    @property
    def hc1_mixer_valve(self):
        """Supply temperature of heating circuit 1"""
        return self._heating_circuit_input_regs.get('HC_1_MIXER_VALVE')['value']

    @property
    def hc1_state(self):
        """Supply temperature of heating circuit 1"""
        return self._heating_circuit_input_regs.get('HC_1_MIXER_VALVE')['value']
        #return HEATING_STATE.get(value, "UNKOWN")

    @property
    def bu1_top_temp(self):
        """Supply temperature of heating circuit 1"""
        return self._buffer_input_regs.get('BU_1_TOP_TEMPERATURE')['value']
    
    @property
    def bu1_bottom_temp(self):
        """Supply temperature of heating circuit 1"""
        return self._buffer_input_regs.get('BU_1_BOTTOM_TEMPERATURE')['value']
    
    @property
    def bu1_pump(self):
        """Supply temperature of heating circuit 1"""
        return self._buffer_input_regs.get('BU_1_PUMP')['value']
    
    @property
    def bu1_state(self):
        """Supply temperature of heating circuit 1"""
        return self._buffer_input_regs.get('BU_1_STATE')['value']
        #return BUFFER_STATE.get(value, "UNKOWN")
    
    @property
    def bu1_mode(self):
        """Supply temperature of heating circuit 1"""
        return self._buffer_input_regs.get('BU_1_MODE')['value']
        #return BUFFER_MODE.get(value, "UNKOWN")

    @property
    def bo1_temp(self):
        """Supply temperature of heating circuit 1"""
        return self._boiler_input_regs.get('BO_1_TEMPERATURE')['value']

    @property
    def bo1_state(self):
        """Supply temperature of heating circuit 1"""
        return self._boiler_input_regs.get('BO_1_STATE')['value']
        #return BOILER_STATE.get(value, "UNKOWN")

    @property
    def bo1_mode(self):
        """Supply temperature of heating circuit 1"""
        return self._boiler_input_regs.get('BO_1_MODE')['value']
        #return BOILER_MODE.get(value, "UNKOWN")

    @property
    def hp_supply_temp(self):
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get('SUPPLY_TEMPERATURE')['value']

    @property
    def hp_return_temp(self):
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get('RETURN_TEMPERATURE')['value']

    @property
    def hp_flow_rate(self):
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get('FLOW_RATE')['value']

    @property
    def hp_compressor_speed(self):
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get('COMPRESSOR_SPEED')['value']

    @property
    def hp_evu_lock_active(self):
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get('EVU_LOCK_ACTIVE')['value']
        #return EVU_LOCK.get(value, "UNKNOWN")

    @property
    def hp_defrost_active(self):
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get('DEFROST_ACTIVE')['value']
        #return DEFROST.get(value, "UNKNOWN")

    @property
    def hp_boiler_charge(self):
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get('BOILER_CHARGE')['value']
        #return BOILER_CHARGE.get(value, "UNKNOWN")

    @property
    def hp_thermal_energy_total(self):
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get('THERMAL_ENERGY_TOTAL')['value']

    @property
    def hp_thermal_energy_drinking_water(self):
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get('THERMAL_ENERGY_DRINKING_WATER')['value']

    @property
    def hp_thermal_energy_heating(self):
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get('THERMAL_ENERGY_HEATING')['value']

    @property
    def hp_electrical_energy_total(self):
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get('ELECTRICAL_ENERGY_TOTAL')['value']

    @property
    def hp_electrical_energy_drinking_water(self):
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get('ELECTRICAL_ENERGY_DRINKING_WATER')['value']

    @property
    def hp_eletrical_energy_heating(self):
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get('ELECTRICAL_ENERGY_HEATING')['value']

    @property
    def hp_electrical_power(self):
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get('ELECTRICAL_POWER')['value']

    @property
    def hp_thermal_power_cooling(self):
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get('THERMAL_POWER_COOLING')['value']

    @property
    def hp_thermal_power_heating(self):
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get('THERMAL_POWER_HEATING')['value']

    @property
    def hp_thermal_energy_cooling(self):
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get('THERMAL_ENERGY_COOLING')['value']

    @property
    def hp_electrical_energy_cooling(self):
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get('ELECTRICAL_ENERGY_COOLING')['value']

    @property
    def hp_cop(self):
        """Supply temperature of heating circuit 1"""
        if self.hp_electrical_power: 
            return self.hp_thermal_power_heating / self.hp_electrical_power
        return 0.0

    @property
    def hp_vampair_state(self):
        """Supply temperature of heating circuit 1"""
        return self._heatpump_input_regs.get('VAMPAIR_STATE')['value']
        #return VAMPAIR_STATE.get(value, "UNKOWN")

    @property
    def pv_power(self):
        """Supply temperature of heating circuit 1"""
        return self._photovoltaik_input_regs.get('PV_POWER')['value']

    @property
    def pv_house_consumption(self):
        """Supply temperature of heating circuit 1"""
        return self._photovoltaik_input_regs.get('HOUSE_CONSUMPTION')['value']

    @property
    def pv_heatpump_consumption(self):
        """Supply temperature of heating circuit 1"""
        return self._photovoltaik_input_regs.get('HEATPUMP_CONSUMPTION')['value']

    @property
    def pv_grid_import(self):
        """Supply temperature of heating circuit 1"""
        return self._photovoltaik_input_regs.get('GRID_IMPORT')['value']

    @property
    def pv_grid_export(self):
        """Supply temperature of heating circuit 1"""
        return self._photovoltaik_input_regs.get('GRID_EXPORT')['value']

    def __init__(self, conn, update_on_read=False):
        """Initialize Solarfocus communication."""
        self._conn = conn
        self._heating_circuit_input_regs = HC_REGMAP_INPUT
        self._buffer_input_regs = BU_REGMAP_INPUT
        self._boiler_input_regs = BO_REGMAP_INPUT
        self._heatpump_input_regs = HP_REGMAP_INPUT
        self._photovoltaik_input_regs = PV_REGMAP_INPUT
        self._slave = SLAVE_ID
        self._update_on_read = update_on_read

    def connect(self):
        """ Connect to Solarfocus eco manager-touch """
        return self._conn.connect()

    def update(self):
        """Read values from Heating System"""
        ret = True
        try:
            hc_result_input = self._conn.read_input_registers(
                address=HC_START_ADDR,
                count=HC_COUNT).registers

            bu_result_input = self._conn.read_input_registers(
                unit=self._slave,
                address=BU_START_ADDR,
                count=BU_COUNT).registers

            bo_result_input = self._conn.read_input_registers(
                unit=self._slave,
                address=BO_START_ADDR,
                count=BO_COUNT).registers

            hp_result_input = self._conn.read_input_registers(
                unit=self._slave,
                address=HP_START_ADDR,
                count=HP_COUNT).registers

            pv_result_input = self._conn.read_input_registers(
                unit=self._slave,
                address=PV_START_ADDR,
                count=PV_COUNT).registers
        except AttributeError:
            # The unit does not reply reliably
            ret = False
            print("Modbus read failed")

        else:
            self._parseRegisters(self._heating_circuit_input_regs, hc_result_input)
            self._parseRegisters(self._buffer_input_regs, bu_result_input)
            self._parseRegisters(self._boiler_input_regs, bo_result_input)
            self._parseRegisters(self._heatpump_input_regs, hp_result_input)
            self._parseRegisters(self._photovoltaik_input_regs, pv_result_input)

        return ret

    def _parseRegisters(self, input_reg, result_reg):
        for i in input_reg:
            _entry = input_reg[i]
            _idx = _entry["addr"]
            _value = result_reg[_idx]

            # Multi-register values (UINT32, INT32)
            if _entry['count'] == 2:
                _value = (result_reg[_idx] << 16) + result_reg[_idx+1]
            else:
                _value = result_reg[_idx]
            
            # Datatype
            if _entry["type"] is INT:
                _value = self._unsignedToSigned(_value, _entry['count']*2)

            # Scale
            _value*=_entry["multiplier"]

            # Store
            input_reg[i]["value"] = _value

    def _unsignedToSigned(self, n, byte_count): 
        return int.from_bytes(n.to_bytes(byte_count, 'little', signed=False), 'little', signed=True)

            