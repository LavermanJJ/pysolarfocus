"""Constants for pysolarfocs"""
from enum import Enum
import logging

class RegisterTypes(str, Enum):
    Holding = "Holding"
    Input = "Input"
     
class DataTypes(int, Enum):
    INT = 1
    UINT = 2  
    
    
    
class DataValue(object):
    """
    Abstraction of a certain relative address in the modbus register
    """
    type:DataTypes
    address:int
    count:int
    value:int
    multiplier:float|None
    _absolut_address:int
    register_type:RegisterTypes
    def __init__(self,address:int,count:int=1,default_value:int=0,multiplier:float=None,type:DataTypes=DataTypes.INT,register_type:RegisterTypes=RegisterTypes.Input) -> None:
        self.address = address
        self.count = count
        self.value = default_value
        self.multiplier = multiplier
        self.type = type
        self._absolut_address = None # This will be set by the parent component
        self.register_type = register_type
        
    def get_absolute_address(self)->int:
        """
        Returns the absolute address of the register
        """
        if not self._absolut_address:
            raise Exception("Absolute address not set!")
        return self._absolut_address + self.address  
    
    @property
    def has_scaler(self)->bool:
        return  self.multiplier is not None
    
    @property
    def scaled_value(self)->float:
        if self.has_scaler:
            return self.value / self.multiplier
        else:
            return self.value
        
    def set_unscaled_value(self,value:float)->None:
        """
        Applies the scaler to the value and sets the value
        """
        if self.has_scaler:
            self.value = int(value*self.multiplier)
        else:
            self.value = value
    
    
class Component(object):
    def __init__(self,input_address:int,input_count:int,holding_address:int=-1,holding_count:int=-1)->None:
        self.input_address = input_address
        self.input_count = input_count
        self.holding_address = holding_address
        self.holding_count = holding_count
        self.__data_values = None
        
    def _initialize_addresses(self)->None:
        """
        Initializes the absolute addresses of the DataValues
        """
        for _,value in self.__get_data_values():
            if value.register_type == RegisterTypes.Input:
                value._absolut_address = self.input_address
            else:
                value._absolut_address = self.holding_address
                
    @property
    def has_input_address(self)->bool:
        return self.input_address >= 0 and self.input_count > 0
    
    @property
    def has_holding_address(self)->bool:
        return self.holding_address >= 0 and self.holding_count > 0
        
    def __get_data_values(self)->list[tuple[str,DataValue]]:
        """
        Returns all DataValues of this Component
        """
        if self.__data_values is None:
            self.__data_values = [(k,v) for k,v in self.__dict__.items() if isinstance(v,DataValue)]
        return self.__data_values
    
    def __get_input_values(self)->list[tuple[str,DataValue]]:
        return [(k,v) for k,v in self.__get_data_values() if v.register_type == RegisterTypes.Input]
    
    def __get_holding_values(self)->list[tuple[str,DataValue]]:
        return [(k,v) for k,v in self.__get_data_values() if v.register_type == RegisterTypes.Holding]
    
    @staticmethod
    def __unsigned_to_signed(n:int, byte_count:int)->int:
        return int.from_bytes(
            n.to_bytes(byte_count, "little", signed=False), "little", signed=True
        )
        
    def parse(self,data:list[int],type:RegisterTypes)->bool:
        """
        Dynamically assignes the values to the DataValues of this Component
        """
        if len(data) != (self.input_count if type == RegisterTypes.Input else self.holding_count):
            logging.error(f"Data length does not match the expected length of {self.count} for {self.__class__.__name__}")
            return False
        
        encountered_error = False
        for name,value in self.__get_input_values() if type == RegisterTypes.Input else self.__get_holding_values():
            try:
                # Multi-register values (UINT32, INT32)
                if value.count == 2:
                    _value = (data[value.address] << 16) + data[value.address+ 1]
                else:
                    _value = data[value.address]
                 
                # Datatype
                if value.type == DataTypes.INT:
                    _value = Component.__unsigned_to_signed(_value, value.count * 2)
                    
                #Store
                value.value = _value   
            except:
                logging.exception(f"Error while parsing {name} of {self.__class__.__name__}")
                encountered_error = True
        return not encountered_error

        
        
        

        


INT = 1
UINT = 2

# Values provided by Solarfocus manual
PORT = 502
SLAVE_ID = 1

class HeatingCircuit(Component):
    def __init__(self) -> None:
        super().__init__(input_address=1100,input_count=7,holding_address=32600,holding_count=8)
        self.supply_temperature = DataValue(address=0,multiplier=0.1)
        self.room_temperature = DataValue(address=1,multiplier=0.1)
        self.humidity = DataValue(address=2,multiplier=0.1)
        self.limit_temperature = DataValue(address=3,type=DataTypes.UINT)
        self.circulator_pump = DataValue(address=4,type=DataTypes.UINT)
        self.mixer_valve = DataValue(address=5,type=DataTypes.UINT)
        self.state = DataValue(address=6,type=DataTypes.UINT)
        
        self.target_supply_temperature = DataValue(address=0,multiplier=10,register_type=RegisterTypes.Holding)
        self.cooling = DataValue(address=2,register_type=RegisterTypes.Holding)
        self.mode = DataValue(address=3,register_type=RegisterTypes.Holding)
        self.target_room_temperatur = DataValue(address=5,multiplier=10,register_type=RegisterTypes.Holding)
        self.indoor_temperatur_external = DataValue(address=6,multiplier=10,register_type=RegisterTypes.Holding)
        self.indoor_humidity_external = DataValue(address=7,register_type=RegisterTypes.Holding)
        self._initialize_addresses()
        
        
HC_START_ADDR = 1100
HC_COUNT = 7
HC_REGMAP_INPUT = {
    "HC_1_SUPPLY_TEMPERATURE": {
        "addr": 0,
        "value": 0,
        "multiplier": 0.1,
        "count": 1,
        "type": INT,
    },
    "HC_1_ROOM_TEMPERATURE": {
        "addr": 1,
        "value": 0,
        "multiplier": 0.1,
        "count": 1,
        "type": INT,
    },
    "HC_1_HUMIDITY": {
        "addr": 2,
        "value": 0,
        "multiplier": 0.1,
        "count": 1,
        "type": INT,
    },
    "HC_1_LIMIT_THERMOSTAT": {
        "addr": 3,
        "value": 0,
        "multiplier": 1,
        "count": 1,
        "type": UINT,
    },
    "HC_1_CIRCULATOR_PUMP": {
        "addr": 4,
        "value": 0,
        "multiplier": 1,
        "count": 1,
        "type": UINT,
    },
    "HC_1_MIXER_VALVE": {
        "addr": 5,
        "value": 0,
        "multiplier": 1,
        "count": 1,
        "type": UINT,
    },
    "HC_1_STATE": {"addr": 6, "value": 0, "multiplier": 1, "count": 1, "type": UINT},
}

class Buffer(Component):
    def __init__(self) -> None:
        super().__init__(1900, 5)
        self.top_temperature = DataValue(address=0,multiplier=0.1)
        self.bottom_temperature = DataValue(address=1,multiplier=0.1)
        self.pump = DataValue(address=2)
        self.state = DataValue(address=3,type=DataTypes.UINT)
        self.mode = DataValue(address=4,type=DataTypes.UINT)
        
        self._initialize_addresses()
        
BU_START_ADDR = 1900
BU_COUNT = 5
BU_REGMAP_INPUT = {
    "BU_1_TOP_TEMPERATURE": {
        "addr": 0,
        "value": 0,
        "multiplier": 0.1,
        "count": 1,
        "type": INT,
    },
    "BU_1_BOTTOM_TEMPERATURE": {
        "addr": 1,
        "value": 0,
        "multiplier": 0.1,
        "count": 1,
        "type": INT,
    },
    "BU_1_PUMP": {"addr": 2, "value": 0, "multiplier": 1, "count": 1, "type": INT},
    "BU_1_STATE": {"addr": 3, "value": 0, "multiplier": 1, "count": 1, "type": UINT},
    "BU_1_MODE": {"addr": 4, "value": 0, "multiplier": 1, "count": 1, "type": UINT},
}

class Boiler(Component):
    def __init__(self) -> None:
        super().__init__(input_address=500, input_count=3, holding_address=32000, holding_count=4)
        self.temperature = DataValue(address=0,multiplier=0.1)
        self.state = DataValue(address=1,type=DataTypes.UINT)
        self.mode = DataValue(address=2,type=DataTypes.UINT)
        
        self.target_temperature = DataValue(address=0,multiplier=10,register_type=RegisterTypes.Holding)
        self.single_charge = DataValue(address=1,register_type=RegisterTypes.Holding)
        self.mode= DataValue(address=2,register_type=RegisterTypes.Holding)
        self.circulation = DataValue(address=3,register_type=RegisterTypes.Holding)
        
        self._initialize_addresses()

BO_START_ADDR = 500
BO_COUNT = 3
BO_REGMAP_INPUT = {
    "BO_1_TEMPERATURE": {
        "addr": 0,
        "value": 0,
        "multiplier": 0.1,
        "count": 1,
        "type": INT,
    },
    "BO_1_STATE": {"addr": 1, "value": 0, "multiplier": 1, "count": 1, "type": UINT},
    "BO_1_MODE": {"addr": 2, "value": 0, "multiplier": 1, "count": 1, "type": UINT},
}

class HeatPump(Component):
    def __init__(self) -> None:
        super().__init__(input_address=2300, input_count=27,holding_address=33404, holding_count=3)
        self.supply_temperature = DataValue(address=0,multiplier=0.1)
        self.return_temperatur = DataValue(address=1,multiplier=0.1)
        self.flow_rate = DataValue(address=2)
        self.compressor_speed = DataValue(address=3)
        self.evu_lock_active = DataValue(address=4,type=DataTypes.UINT)
        self.defrost_active = DataValue(address=5,type=DataTypes.UINT)
        self.boilder_charge = DataValue(address=6, type=DataTypes.UINT)
        self.thermal_energy_total = DataValue(address=7,count=2,multiplier=0.001)
        self.thermal_energy_drinking_water = DataValue(address=9,count=2,multiplier=0.001)
        self.thermal_energy_heating = DataValue(address=11,count=2,multiplier=0.001)
        self.electrical_energy_total = DataValue(address=13,count=2,multiplier=0.001)
        self.electrical_energy_drinking_water = DataValue(address=15,count=2,multiplier=0.001)
        self.electrical_energy_heating = DataValue(address=17,count=2,multiplier=0.001)
        self.electrical_power = DataValue(address=19)
        self.thermal_power_cooling = DataValue(address=20)
        self.thermal_power_heating = DataValue(address=21)
        self.thermal_energy_cooling = DataValue(address=22,count=2,multiplier=0.001,type=DataTypes.UINT)
        self.electrical_energy_cooling = DataValue(address=24,count=2,multiplier=0.001,type=DataTypes.UINT)
        self.vampair_state = DataValue(address=26,type=DataTypes.UINT)
        
        self.evu_lock = DataValue(address=0,register_type=RegisterTypes.Holding)
        self.smart_grid = DataValue(address=1,register_type=RegisterTypes.Holding)
        self.outdoor_temperature_external = DataValue(address=2,multiplier=10,register_type=RegisterTypes.Holding)
        self._initialize_addresses()
        
        
HP_START_ADDR = 2300
HP_COUNT = 27
HP_REGMAP_INPUT = {
    "SUPPLY_TEMPERATURE": {
        "addr": 0,
        "value": 0,
        "multiplier": 0.1,
        "count": 1,
        "type": INT,
    },
    "RETURN_TEMPERATURE": {
        "addr": 1,
        "value": 0,
        "multiplier": 0.1,
        "count": 1,
        "type": INT,
    },
    "FLOW_RATE": {"addr": 2, "value": 0, "multiplier": 1, "count": 1, "type": INT},
    "COMPRESSOR_SPEED": {
        "addr": 3,
        "value": 0,
        "multiplier": 1,
        "count": 1,
        "type": INT,
    },
    "EVU_LOCK_ACTIVE": {
        "addr": 4,
        "value": 0,
        "multiplier": 1,
        "count": 1,
        "type": UINT,
    },
    "DEFROST_ACTIVE": {
        "addr": 5,
        "value": 0,
        "multiplier": 1,
        "count": 1,
        "type": UINT,
    },
    "BOILER_CHARGE": {"addr": 6, "value": 0, "multiplier": 1, "count": 1, "type": UINT},
    "THERMAL_ENERGY_TOTAL": {
        "addr": 7,
        "value": 0,
        "multiplier": 0.001,
        "count": 2,
        "type": INT,
    },
    "THERMAL_ENERGY_DRINKING_WATER": {
        "addr": 9,
        "value": 0,
        "multiplier": 0.001,
        "count": 2,
        "type": INT,
    },
    "THERMAL_ENERGY_HEATING": {
        "addr": 11,
        "value": 0,
        "multiplier": 0.001,
        "count": 2,
        "type": INT,
    },
    "ELECTRICAL_ENERGY_TOTAL": {
        "addr": 13,
        "value": 0,
        "multiplier": 0.001,
        "count": 2,
        "type": INT,
    },
    "ELECTRICAL_ENERGY_DRINKING_WATER": {
        "addr": 15,
        "value": 0,
        "multiplier": 0.001,
        "count": 2,
        "type": INT,
    },
    "ELECTRICAL_ENERGY_HEATING": {
        "addr": 17,
        "value": 0,
        "multiplier": 0.001,
        "count": 2,
        "type": INT,
    },
    "ELECTRICAL_POWER": {
        "addr": 19,
        "value": 0,
        "multiplier": 1,
        "count": 1,
        "type": INT,
    },
    "THERMAL_POWER_COOLING": {
        "addr": 20,
        "value": 0,
        "multiplier": 1,
        "count": 1,
        "type": INT,
    },
    "THERMAL_POWER_HEATING": {
        "addr": 21,
        "value": 0,
        "multiplier": 1,
        "count": 1,
        "type": INT,
    },
    "THERMAL_ENERGY_COOLING": {
        "addr": 22,
        "value": 0,
        "multiplier": 0.001,
        "count": 2,
        "type": UINT,
    },
    "ELECTRICAL_ENERGY_COOLING": {
        "addr": 24,
        "value": 0,
        "multiplier": 0.001,
        "count": 2,
        "type": UINT,
    },
    "VAMPAIR_STATE": {
        "addr": 26,
        "value": 0,
        "multiplier": 1,
        "count": 1,
        "type": UINT,
    },
}


class Photovoltaic(Component):
    def __init__(self) -> None:
        super().__init__(input_address=2500, input_count=10, holding_address=33407,holding_count=3)
        self.power = DataValue(address=0,count=2)
        self.house_consumption = DataValue(address=2,count=2)
        self.heatpump_consumption = DataValue(address=4,count=2)
        self.grid_import = DataValue(address=6,count=2)
        self.grid_export = DataValue(address=8,count=2)
        
        self.smart_meter = DataValue(address=0,register_type=RegisterTypes.Holding)
        self.photovoltaic = DataValue(address=1,register_type=RegisterTypes.Holding)
        self.grid_im_export = DataValue(address=2,register_type=RegisterTypes.Holding)
        
        self._initialize_addresses()
        
PV_START_ADDR = 2500
PV_COUNT = 10
PV_REGMAP_INPUT = {
    "PV_POWER": {"addr": 0, "value": 0, "multiplier": 1, "count": 2, "type": INT},
    "HOUSE_CONSUMPTION": {
        "addr": 2,
        "value": 0,
        "multiplier": 1,
        "count": 2,
        "type": INT,
    },
    "HEATPUMP_CONSUMPTION": {
        "addr": 4,
        "value": 0,
        "multiplier": 1,
        "count": 2,
        "type": INT,
    },
    "GRID_IMPORT": {"addr": 6, "value": 0, "multiplier": 1, "count": 2, "type": INT},
    "GRID_EXPORT": {"addr": 8, "value": 0, "multiplier": 1, "count": 2, "type": INT},
}


class PelletsBoiler(Component):
    def __init__(self) -> None:
        super().__init__(2400, 13)
        self.temperature = DataValue(address=0,multiplier=0.1)
        self.status  = DataValue(address=1,type=DataTypes.UINT)
        self.message_number = DataValue(address=4)
        self.door_contact = DataValue(address=5)
        self.cleaning = DataValue(address=6)
        self.ash_container = DataValue(address=7)
        self.outdoor_temperature = DataValue(address=8,multiplier=0.1)
        self.octoplus_buffer_temperature_bottom = DataValue(address=9,multiplier=0.1)
        self.octoplus_buffer_temperature_top = DataValue(address=10,multiplier=0.1)
        self.log_wood = DataValue(address=11,type=DataTypes.UINT)
        
PB_START_DDR = 2400
PB_COUNT = 13
PB_REGMAP_INPUT = {
    "PELLETSBOILER_TEMPERATURE": {"addr": 0, "value": 0, "multiplier": 0.1, "count": 1, "type": INT},
    "STATUS": {"addr": 1, "value": 0, "multiplier": 1, "count": 1, "type": UINT},
    "MESSAGE_NUMBER": {"addr": 4, "value": 0, "multiplier": 1, "count": 1, "type": INT},
    "DOOR_CONTACT": {"addr": 5, "value": 0, "multiplier": 1, "count": 1, "type": INT},
    "CLEANING": {"addr": 6, "value": 0, "multiplier": 1, "count": 1, "type": INT},
    "ASH_CONTAINER": {"addr": 7, "value": 0, "multiplier": 1, "count": 1, "type": INT},
    "OUTDOOR_TEMPERATURE": {"addr": 8, "value": 0, "multiplier": 0.1, "count": 1, "type": INT},
    #"MODE_THERMINATOR": {"addr": 9, "value": 0, "multiplier": 1, "count": 1, "type": INT},
    "OCTOPLUS_BUFFER_TEMPERATURE_BOTTOM": {"addr": 9, "value": 0, "multiplier": 0.1, "count": 1, "type": INT},
    "OCTOPLUS_BUFFER_TEMPERATURE_TOP": {"addr": 10, "value": 0, "multiplier": 0.1, "count": 1, "type": INT},
    "LOG_WOOD_THERMINATOR": {"addr": 11, "value": 0, "multiplier": 1, "count": 1, "type": UINT},
}


HC_REGMAP_HOLDING = {
    "TARGET_SUPPLY_TEMPERATURE": {
        "addr": 32600,
        "value": 0,
        "multiplier": 10,
        "count": 1,
        "type": INT,
    },
    "COOLING": {"addr": 32602, "value": 0, "multiplier": 1, "count": 1, "type": INT},
    "MODE": {"addr": 32603, "value": 0, "multiplier": 1, "count": 1, "type": INT},
    "TARGET_ROOM_TEMPERATURE": {
        "addr": 32605,
        "value": 0,
        "multiplier": 10,
        "count": 1,
        "type": INT,
    },
    "INDOOR_TEMPERATURE_EXTERNAL": {
        "addr": 32606,
        "value": 0,
        "multiplier": 10,
        "count": 1,
        "type": INT,
    },
    "INDOOR_HUMIDITY_EXTERNAL": {
        "addr": 32607,
        "value": 0,
        "multiplier": 1,
        "count": 1,
        "type": INT,
    },
}

BO_REGMAP_HOLDING = {
    "TARGET_TEMPERATURE": {
        "addr": 32000,
        "value": 0,
        "multiplier": 10,
        "count": 1,
        "type": INT,
    },
    "SINGLE_CHARGE": {
        "addr": 32001,
        "value": 0,
        "multiplier": 1,
        "count": 1,
        "type": INT,
    },
    "MODE": {"addr": 32002, "value": 0, "multiplier": 1, "count": 1, "type": INT},
    "CIRCULATION": {
        "addr": 32003,
        "value": 0,
        "multiplier": 1,
        "count": 1,
        "type": INT,
    },
}

HP_REGMAP_HOLDING = {
    "EVU_LOCK": {"addr": 33404, "value": 0, "multiplier": 1, "count": 1, "type": INT},
    "SMART_GRID": {"addr": 33405, "value": 0, "multiplier": 1, "count": 1, "type": INT},
    "OUTDOOR_TEMPERATURE_EXTERNAL": {
        "addr": 33406,
        "value": 0,
        "multiplier": 10,
        "count": 1,
        "type": INT,
    },
}

PV_REGMAP_HOLDING = {
    "SMART_METER": {
        "addr": 33407,
        "value": 0,
        "multiplier": 1,
        "count": 1,
        "type": INT,
    },
    "PHOTOVOLTAIC": {
        "addr": 33408,
        "value": 0,
        "multiplier": 1,
        "count": 1,
        "type": INT,
    },
    "GRID_IM_EXPORT": {
        "addr": 33409,
        "value": 0,
        "multiplier": 1,
        "count": 1,
        "type": INT,
    },
}


HEATING_STATE = {
    0: "Heizkreis ist ausgeschaltet",
    1: "Absenkbetrieb",
    2: "Heizbetrieb",
    3: "Ferienbetrieb",
    4: "Estrichprogramm",
    5: "Frostschutzbetrieb",
    6: "Kaminkehrer",
    7: "Heizkreis nicht freigeschaltet",
    8: "Wärmeableitung",
    9: "Außenabschalttemperatur Heizbetrieb erreicht",
    10: "Raumsolltemperatur Heizbetrieb erreicht",
    11: "Trinkwasserspeichervorrang ist aktiv",
    12: "Dauerheizbetrieb",
    13: "Dauerabsenkbetrieb",
    14: "Aussenfühlerunterbrechung",
    15: "min. Energiequellentemperatur unterschritten",
    16: "Vorlauffühler defekt",
    17: "min. Energiequellentemperatur unterschritten, Frostschutzbetrieb",
    18: "Testlauf Pumpe ist aktiv",
    19: "Partybetrieb",
    20: "Begrenzungsthermostat ist offen",
    21: "Pumpen Nachlauf",
    22: "Defrost",
    23: "Kühlbetrieb",
    24: "Kühlen hat Vorrang",
    25: "Heizen hat Vorrang",
    26: "Pool hat Vorrang",
    27: "Außenabschalttemperatur Absenkbetrieb erreicht",
    28: "Raumsolltemperatur Absenkbetrieb erreicht",
    29: "Min. Rücklauftemperatur – Regelung vampair",
    30: "Außenabschalttemperatur Kühlen erreicht",
    31: "warte auf Kühlbetrieb der Wärmepumpe",
}

BUFFER_STATE = {
    0: "Status nicht vorhanden",
    1: "Bereitschaft",
    2: "Puffer wird beladen",
    3: "Frostschutzbetrieb",
    4: "Kaminkehrer",
    5: "Wärmeableitung",
    6: "Testlauf Pumpe ist aktiv ",
    7: "Trinkwasserspeicher wird beladen",
}

BUFFER_MODE = {0: "Immer Aus", 1: "Immer Ein", 2: "Zeitschaltung"}

BOILER_STATE = {
    0: "Boilerstatus nicht vorhanden",
    1: "Bereitschaft",
    2: "Laden",
    3: "Frostschutz",
    4: "Rauchfangkehrermodus",
    5: "Legionellenschutz",
    6: "Anforderung",
    7: "Energiequelle zu heiß",
    8: "Blockadeschutz",
    9: "einmalige Freigabe aktiv",
    10: "Fühler Kurzschluss",
    11: "Fühler Unterbrechung",
    12: "Ferienbetrieb",
    13: "Defrost",
}

BOILER_MODE = {
    0: "Immer Aus",
    1: "Immer Ein",
    2: "Montag – Sonntag",
    3: "Blockweise (Montag – Freitag, Samstag – Sonntag)",
    4: "Tagweise",
}

EVU_LOCK = {
    0: "Normalbetrieb",
    1: "EVU-Lock Aktiv",
}

DEFROST = {
    0: "Abtauung nicht aktiv",
    1: "Abtauung aktiv",
}

BOILER_CHARGE = {
    0: "Boilerladung nicht aktiv",
    1: "Boilerladung aktiv",
}

VAMPAIR_STATE = {
    0: "Bereitschaft",
    1: "Heizbetrieb",
    2: "Heizbetrieb, Trinkwasserspeicherladung",
    3: "Kühlbetrieb",
    4: "Manueller Betrieb",
    5: "EVU-Lock aktiv",
    6: "keine Zeitfreigabe, Wärmepumpe aus",
    7: "Außentemperatursperre, Wärmepumpe aus",
    8: "elektrische Zusatzheizung aktiv",
    9: "Fremdkessel aktiv, Wärmepumpe aus",
    10: "Kühlanforderung",
    11: "manuelle Leistungsvorgabe",
    12: "Wärmepumpe ausgeschaltet",
}

SMART_GRID_EINSCHALTUNG = 4
SMART_GRID_NORMALBETRIEB = 2
