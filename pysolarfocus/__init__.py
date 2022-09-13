"""Python client lib for Solarfocus"""
__version__ = "1.2.1"


from .const import (
    BO_COUNT,
    BO_REGMAP_HOLDING,
    BO_REGMAP_INPUT,
    BO_START_ADDR,
    BU_COUNT,
    BU_REGMAP_INPUT,
    BU_START_ADDR,
    HC_COUNT,
    HC_REGMAP_HOLDING,
    HC_REGMAP_INPUT,
    HC_START_ADDR,
    HP_COUNT,
    HP_REGMAP_HOLDING,
    HP_REGMAP_INPUT,
    HP_START_ADDR,
    INT,
    PB_COUNT,
    PB_REGMAP_INPUT,
    PB_START_DDR,
    PV_COUNT,
    PV_REGMAP_HOLDING,
    PV_REGMAP_INPUT,
    PV_START_ADDR,
    SLAVE_ID,
    SMART_GRID_EINSCHALTUNG,
    SMART_GRID_NORMALBETRIEB,
)


class SolarfocusAPI:
    """Solarfocus Heating System"""

    @property
    def hc1_supply_temp(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self._heating_circuit_input_regs.get("HC_1_SUPPLY_TEMPERATURE")["value"]

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
    def pb_mode(self) -> int:
        """Supply temperature of heating circuit 1"""
        return self._pelletsboiler_input_regs.get("MODE_THERMINATOR")["value"]

    @property
    def pb_octoplus_buffer_temperature_bottom(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self._pelletsboiler_input_regs.get("OCTOPLUS_BUFFER_TEMPERATURE_BOTTOM")["value"]

    @property
    def pb_octoplus_buffer_temperature_top(self) -> float:
        """Supply temperature of heating circuit 1"""
        return self._pelletsboiler_input_regs.get("OCTOPLUS_BUFFER_TEMPERATURE_TOP")["value"]



    def __init__(self, conn, update_on_read=False):
        """Initialize Solarfocus communication."""
        self._conn = conn
        self._heating_circuit_input_regs = HC_REGMAP_INPUT
        self._heating_circuit_holding_regs = HC_REGMAP_HOLDING
        self._buffer_input_regs = BU_REGMAP_INPUT
        self._boiler_input_regs = BO_REGMAP_INPUT
        self._boiler_holding_regs = BO_REGMAP_HOLDING
        self._heatpump_input_regs = HP_REGMAP_INPUT
        self._heatpump_holding_regs = HP_REGMAP_HOLDING
        self._photovoltaic_input_regs = PV_REGMAP_INPUT
        self._photovoltaic_holidng_regs = PV_REGMAP_HOLDING
        self._pelletsboiler_input_regs = PB_REGMAP_INPUT
        self._slave = SLAVE_ID
        self._update_on_read = update_on_read

    def connect(self):
        """Connect to Solarfocus eco manager-touch"""
        return self._conn.connect()

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
        result_input = self._update_input(
            HC_START_ADDR, HC_COUNT, self._heating_circuit_input_regs
        )
        result_holding = self._update_holding(self._heating_circuit_holding_regs)
        return result_input or result_holding

    def update_buffer(self) -> bool:
        """Read values from Heating System"""
        return self._update_input(BU_START_ADDR, BU_COUNT, self._buffer_input_regs)

    def update_boiler(self) -> bool:
        """Read values from Heating System"""
        result_input = self._update_input(
            BO_START_ADDR, BO_COUNT, self._boiler_input_regs
        )
        result_holding = self._update_holding(self._boiler_holding_regs)
        return result_input or result_holding

    def update_heatpump(self) -> bool:
        """Read values from Heating System"""
        result_input = self._update_input(
            HP_START_ADDR, HP_COUNT, self._heatpump_input_regs
        )
        result_holding = self._update_holding(self._heatpump_holding_regs)
        return result_input or result_holding

    def update_photovoltaic(self) -> bool:
        """Read values from Heating System"""
        result_input = self._update_input(
            PV_START_ADDR, PV_COUNT, self._photovoltaic_input_regs
        )
        result_holding = self._update_holding(self._photovoltaic_holidng_regs)
        return result_input or result_holding

    def update_pelletsboiler(self) -> bool:
        """Read values from Pellets boiler"""
        result_input = self._update_input(
            PB_START_DDR, PB_COUNT, self._pelletsboiler_input_regs
        )
        return result_input

    def hc1_set_target_supply_temperature(self, temperature) -> bool:
        """Set target supply temperature"""
        temp_scaled = int(
            temperature * HC_REGMAP_HOLDING["TARGET_SUPPLY_TEMPERATURE"]["multiplier"]
        )
        request = self._conn.write_registers(
            HC_REGMAP_HOLDING["TARGET_SUPPLY_TEMPERATURE"]["addr"],
            [temp_scaled],
            unit=SLAVE_ID,
        )
        return not request.isError()

    def hc1_enable_cooling(self, cooling: bool) -> bool:
        """Set target supply temperature"""
        request = self._conn.write_registers(
            HC_REGMAP_HOLDING["COOLING"]["addr"], [int(cooling)], unit=SLAVE_ID
        )
        return not request.isError()

    def hc1_set_mode(self, mode: int) -> bool:
        """Set mode"""
        request = self._conn.write_registers(
            HC_REGMAP_HOLDING["MODE"]["addr"], [mode], unit=SLAVE_ID
        )
        return not request.isError()

    def hc1_set_target_room_temperature(self, temperature: float) -> bool:
        """Set target room temperature"""
        temp_scaled = int(
            temperature * HC_REGMAP_HOLDING["TARGET_ROOM_TEMPERATURE"]["multiplier"]
        )
        request = self._conn.write_registers(
            HC_REGMAP_HOLDING["TARGET_ROOM_TEMPERATURE"]["addr"],
            [temp_scaled],
            unit=SLAVE_ID,
        )
        return not request.isError()

    def hc1_set_indoor_temperature(self, temperature: float) -> bool:
        """Set indoor temperature"""
        temp_scaled = int(
            temperature * HC_REGMAP_HOLDING["INDOOR_TEMPERATURE_EXTERNAL"]["multiplier"]
        )
        request = self._conn.write_registers(
            HC_REGMAP_HOLDING["INDOOR_TEMPERATURE_EXTERNAL"]["addr"],
            [temp_scaled],
            unit=SLAVE_ID,
        )
        return not request.isError()

    def hc1_set_indoor_humidity(self, humidity: float) -> bool:
        """Set indoor humidity"""
        request = self._conn.write_registers(
            HC_REGMAP_HOLDING["INDOOR_HUMIDITY_EXTERNAL"]["addr"],
            [int(humidity)],
            unit=SLAVE_ID,
        )
        return not request.isError()

    def bo1_set_target_temperature(self, temperature: float) -> bool:
        """Set target temperature"""
        temp_scaled = int(
            temperature * BO_REGMAP_HOLDING["TARGET_TEMPERATURE"]["multiplier"]
        )
        request = self._conn.write_registers(
            BO_REGMAP_HOLDING["TARGET_TEMPERATURE"]["addr"],
            [temp_scaled],
            unit=SLAVE_ID,
        )
        return not request.isError()

    def bo1_enable_single_charge(self, enable: bool) -> bool:
        """Enable single charge"""
        request = self._conn.write_registers(
            BO_REGMAP_HOLDING["SINGLE_CHARGE"]["addr"], [int(enable)], unit=SLAVE_ID
        )
        return not request.isError()

    def bo1_set_mode(self, mode: int) -> bool:
        """Set mode"""
        request = self._conn.write_registers(
            BO_REGMAP_HOLDING["MODE"]["addr"], [mode], unit=SLAVE_ID
        )
        return not request.isError()

    def bo1_enable_circulation(self, enable: bool) -> bool:
        """Enable circulation"""
        request = self._conn.write_registers(
            BO_REGMAP_HOLDING["CIRCULATION"]["addr"], [int(enable)], unit=SLAVE_ID
        )
        return not request.isError()

    def hp_smart_grid_request_operation(self, operation_request: bool) -> bool:
        """Set Smart Grid value"""
        if operation_request:
            request = self._conn.write_registers(
                HP_REGMAP_HOLDING["SMART_GRID"]["addr"],
                [SMART_GRID_EINSCHALTUNG],
                unit=SLAVE_ID,
            )
            # self._update_holding(self._heatpump_holding_regs)
            return not request.isError()
        else:
            request = self._conn.write_registers(
                HP_REGMAP_HOLDING["SMART_GRID"]["addr"],
                [SMART_GRID_NORMALBETRIEB],
                unit=SLAVE_ID,
            )
            # self._update_holding(self._heatpump_holding_regs)
            return not request.isError()

    def hp_set_outdoor_temperature(self, temperature: float) -> bool:
        """Set outdoor temperature"""
        temp_scaled = int(
            temperature
            * HP_REGMAP_HOLDING["OUTDOOR_TEMPERATURE_EXTERNAL"]["multiplier"]
        )
        request = self._conn.write_registers(
            HP_REGMAP_HOLDING["OUTDOOR_TEMPERATURE_EXTERNAL"]["addr"],
            [temp_scaled],
            unit=SLAVE_ID,
        )
        return not request.isError()

    def pv_set_smart_meter(self, value: int) -> bool:
        """Set Smart Meter"""
        request = self._conn.write_registers(
            PV_REGMAP_HOLDING["SMART_METER"]["addr"], [value], unit=SLAVE_ID
        )
        return not request.isError()

    def pv_set_photovoltaic(self, value: int) -> bool:
        """Set Photovoltaic"""
        request = self._conn.write_registers(
            PV_REGMAP_HOLDING["PHOTOVOLTAIC"]["addr"], [value], unit=SLAVE_ID
        )
        return not request.isError()

    def pv_set_grid_im_export(self, value: int) -> bool:
        """Set Photovoltaic"""
        request = self._conn.write_registers(
            PV_REGMAP_HOLDING["GRID_IM_EXPORT"]["addr"], [value], unit=SLAVE_ID
        )
        return not request.isError()

    def _update_holding(self, holding_reg) -> bool:
        ret = True
        try:
            for i in holding_reg:
                _entry = holding_reg[i]
                _value = self._conn.read_holding_registers(
                    address=_entry["addr"]
                ).registers[0]

                # Datatype
                if _entry["type"] is INT:
                    _value = self._unsigned_to_signed(_value, _entry["count"] * 2)

                # Scale
                _value /= _entry["multiplier"]

                _entry["value"] = _value
        except AttributeError:
            # The unit does not reply reliably
            ret = False
            print("Modbus read failed")
        else:
            return ret

    def _update_input(self, start: int, count: int, input_reg) -> bool:
        """Read values from Heating System"""
        ret = True
        try:
            result_input = self._conn.read_input_registers(
                address=start, count=count
            ).registers
        except AttributeError:
            # The unit does not reply reliably
            ret = False
            print("Modbus read failed")
        else:
            self._parse_registers(input_reg, result_input)
        return ret

    def _parse_registers(self, input_reg, result_reg):
        for i in input_reg:
            _entry = input_reg[i]
            _idx = _entry["addr"]
            _value = result_reg[_idx]

            # Multi-register values (UINT32, INT32)
            if _entry["count"] == 2:
                _value = (result_reg[_idx] << 16) + result_reg[_idx + 1]
            else:
                _value = result_reg[_idx]

            # Datatype
            if _entry["type"] is INT:
                _value = self._unsigned_to_signed(_value, _entry["count"] * 2)

            # Scale
            _value *= _entry["multiplier"]

            # Store
            input_reg[i]["value"] = _value


    def _unsigned_to_signed(self, n, byte_count):
        print(f"_unsigned_to_signed: n={n}, byte_count={byte_count}")
        return int.from_bytes(
            n.to_bytes(byte_count, "little", signed=False), "little", signed=True
        )

