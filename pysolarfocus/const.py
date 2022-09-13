"""Constants for pysolarfocs"""

INT = 1
UINT = 2

# Values provided by Solarfocus manual
PORT = 502
SLAVE_ID = 1

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

PB_START_DDR = 2400
PB_COUNT = 11
PB_REGMAP_INPUT = {
    "PELLETSBOILER_TEMPERATURE": {"addr": 0, "value": 0, "multiplier": 0.1, "count": 1, "type": INT},
    "STATUS": {"addr": 1, "value": 0, "multiplier": 1, "count": 1, "type": UINT},
    "MESSAGE_NUMBER": {"addr": 2, "value": 0, "multiplier": 1, "count": 1, "type": INT},
    "DOOR_CONTACT": {"addr": 3, "value": 0, "multiplier": 1, "count": 1, "type": INT},
    "CLEANING": {"addr": 4, "value": 0, "multiplier": 1, "count": 1, "type": INT},
    "ASH_CONTAINER": {"addr": 5, "value": 0, "multiplier": 1, "count": 1, "type": INT},
    "OUTDOOR_TEMPERATURE": {"addr": 6, "value": 0, "multiplier": 0.1, "count": 1, "type": INT},
    "MODE_THERMINATOR": {"addr": 7, "value": 0, "multiplier": 1, "count": 1, "type": INT},
    "OCTOPLUS_BUFFER_TEMPERATURE_BOTTOM": {"addr": 8, "value": 0, "multiplier": 0.1, "count": 1, "type": INT},
    "OCTOPLUS_BUFFER_TEMPERATURE_TOP": {"addr": 9, "value": 0, "multiplier": 0.1, "count": 1, "type": INT},
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
