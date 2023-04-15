# pysolarfocus: Python Client for Solarfocus eco<sup>_manager-touch_</sup> via Modbus TCP

Python client library to interact with heating systems of [Solarfocus](https://www.solarfocus.com/) (eco<sup>_manager-touch_</sup> and thermi<sup>nator</sup> II) via Modbus TCP. This library has been developed for the integration into [Home-Assistant](https://www.home-assistant.io/) via a [custom integration](https://github.com/LavermanJJ/home-assistant-solarfocus), but can be used indepdently.

## What's Supported 

### Software Version

This integration has been tested with Solarfocus eco<sup>manager-touch</sup> version `23.020`.

### Systems

* Heat pump vamp<sup>air</sup> with eco<sup>_manager-touch_</sup>
* Biomass boiler thermi<sup>nator</sup> II

### Components

| Components | Supported |
|---|---|
| Heating Circuits (_Heizkreis_) 1-8 | :white_check_mark: |
| Buffers (_Puffer_) 1-4 | :white_check_mark: |
| Solar (_Solar_)| :white_check_mark:|
| Boilers (_Boiler_) 1-4 | :white_check_mark: |
| Heatpump (_Wärmepumpe_) | :white_check_mark: |
| Biomassboiler (_Kessel_) | :white_check_mark: | 
| Photvoltaic (_Photovoltaik_) | :white_check_mark: | 
| Fresh Water Module (_Frischwasser Modul_) 1-4 | :white_check_mark: | 

## How To

### Basic Example 

```python
from pysolarfocus import SolarfocusAPI,Systems,ApiVersions

# Create the Solarfocus API client
solarfocus = SolarfocusAPI(
    ip="solarfocus",                    # adapt IP-Address 
    system=Systems.Vampair,             # for biomass boiler change to Systems.Therminator 
    api_version=ApiVersions.V_23_020)   # select Solarfocus version

solarfocus.connect()
# Fetch the values
solarfocus.update()

# Print the values
print(solarfocus)
print(solarfocus.heating_circuits[0])
```

Output: 

```
--------------------------------------------------
SolarfocusAPI, v3.6.4
--------------------------------------------------
+ API Version: 23.020
+ System: Vampair
+ Components:
  + Heat pump: True
  + Biomass boiler: False
  + Heating circuit: 1
  + Buffer: 1
  + Boiler: 1
  + Fresh water module: 1
  + Solar: False
  + Photovoltaic: False
--------------------------------------------------


============
HeatingCircuit
============
---Input:
supply_temperature| raw:258 scaled:25.8
room_temperature| raw:222 scaled:22.2
humidity| raw:480 scaled:48.0
limit_thermostat| raw:1 scaled:1
circulator_pump| raw:1 scaled:1
mixer_valve| raw:34 scaled:34
state| raw:12 scaled:12
---Holding:
target_supply_temperature | raw:0 scaled:0.0
cooling | raw:0 scaled:0
mode | raw:0 scaled:0
target_room_temperatur | raw:0 scaled:0.0
indoor_temperatur_external | raw:222 scaled:22.2
indoor_humidity_external | raw:480 scaled:48.0
```

### Handling multiple components e.g. heating circuits
Solarfocus systems allow the use of multiple heating circuits, buffers, boilers, and fresh water modules. The api can be configured to interact with multiple components.

```python 
# Create the Solarfocus API client with 2 Heating Circuits
solarfocus = SolarfocusAPI(ip="[Your-IP]",heating_circuit_count=2,system=Systems.Vampair)
# Connect to the heating system
solarfocus.connect()

# Update all heating circuits
solarfocus.update_heating()

# Update only the first heating circuit
solarfocus.heating_circuits[0].update()
# Print the first heating circuit
print(solarfocus.heating_circuits[0])

# Set the temperature of the first heating circuit to 30°C
solarfocus.heating_circuits[0].indoor_temperatur_external.set_unscaled_value(30)
# Write the value to the heating system
solarfocus.heating_circuits[0].indoor_temperatur_external.commit()
```

### API-Version specification
By default, the integration uses API-Version`21.140`. If your system is newer, you can specify
the version by using the `api_version` parameter. 

```python
solarfocus = SolarfocusAPI(ip="[Your-IP]", system=Systems.Vampair, api_version=ApiVersions.V_23_020)
```

You can find the API-Version displayed in the header of the screen of your Solarfocus system:

<img src="images/sf-version.png?raw=true" width="500">

## Changelog of API-Versions
> **Note**
> The API-Version of Solarfocus is independent of the versions of this library. Below list refers to to 
> the Solarfocus versions. See [releases](https://github.com/LavermanJJ/pysolarfocus/releases) for the changelog
> of this library.


#### 23.020
* Add fresh water module state.

#### 23.010
* Add biomass boiler pellet statistics.

#### 22.090
* Add biomass boiler sweep function control.
* Allow input of external buffer values.
