"""Constants for pysolarfocs"""

# Values provided by Solarfocus manual
SLAVE_ID = 1

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
