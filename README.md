[![Version](https://img.shields.io/github/v/tag/lavermanjj/pysolarfocus?style=for-the-badge&label=Version&color=orange)](https://img.shields.io/github/v/tag/lavermanjj/pysolarfocus?style=for-the-badge&label=Version&color=orange)
[![License](https://img.shields.io/github/license/lavermanjj/pysolarfocus?style=for-the-badge)](https://img.shields.io/github/license/lavermanjj/pysolarfocus?style=for-the-badge)


<p align="center">
  <a href="https://github.com/lavermanjj/home-assistant-solarfocus">
    <img src="https://brands.home-assistant.io/solarfocus/logo.png" alt="Logo" height="80">
  </a>
</p>

<h3 align="center">pysolarfocus</h3>

<p align="center">
  Python client for <a href="https://www.solarfocus.com/">Solarfocus</a> eco<sup>manager-touch</sup>  via Modbus TCP
</p>


<details open="open">
  <summary>Table of Contents</summary>

1. [About](#about)
2. [Supported Solarfocus Software and Hardware](#supported-solarfocus-software-and-hardware)
3. [How To](#how-to)
   - [Installation](#installation)
   - [Basic Example](#basic-example)
   - [Handling multiple components](#handling-multiple-components)
   - [Conveniently set modes](#convenitently-set-modes)
   - [API-Version specification](#api-version-specification)
4. [Changelog of API-Versions](#changelog-of-api-versions)


</details>


## About

Python client library to interact with heating systems of [Solarfocus](https://www.solarfocus.com/) (eco<sup>_manager-touch_</sup>) via Modbus TCP. This library has been developed for the integration into [Home-Assistant](https://www.home-assistant.io/) via a [custom integration](https://github.com/LavermanJJ/home-assistant-solarfocus), but can be used indepdently.

> **Warning**
> Use with caution, in case of doubt check with Solarfocus or your installer if a feature / functionality (e.g. cooling) is supported by your installation to avoid damages to your heating system or the building.


## Supported Solarfocus Software and Hardware

### Software

> **Important**
> This integration has been tested with Solarfocus eco<sup>manager-touch</sup> version `25.030`.

Supported versions: `21.140` - `25.030`. Features added in later versions are not yet supported.

The eco<sup>manager-touch</sup> Modbus TCP specification can be found [here](https://www.solarfocus.com/partnerbereich/ecomanager-touch_modbus-tcp_registerdaten_anleitung1.pdf)).

### Hardware

The eco<sup>manager-touch</sup> can integrate the following heating systems
- [Vamp<sup>air</sup>](https://www.solarfocus.com/en/products/air-source-heat-pump-vampair) heat pumps
- [Thermin<sup>nator</sup>](https://www.solarfocus.com/en/products/biomassheating) biomass boilers
- [Ecotop<sup>light</sup> / Ecotop<sup>zero</sup>](https://www.solarfocus.com/de/produkte/biomasseheizung/pelletkessel/ecotop) biomass boilers
- [Octo<sup>plus</sup>](https://www.solarfocus.com/en/products/biomassheating/pellet-boiler/octoplus) biomass boilers
- [Pellet<sup>top</sup>](https://www.solarfocus.com/en/products/biomassheating/pellet-boiler/pellettop) biomass boilers

| Components | Supported |
|---|---|
| Heating Circuit 1 - 8 (_Heizkreis_)| :white_check_mark: |
| Buffer 1 - 4 (_Puffer_) | :white_check_mark: |
| Solar 1 - 4 (_Solar_)| :white_check_mark: |
| Boiler 1 - 4 (_Boiler_) | :white_check_mark: |
| Heat Pump (_Wärmepumpe_) | :white_check_mark: |
| Biomass Boiler (_Kessel_) | :white_check_mark: |
| Fresh Water Module 1 - 4 (_Frischwassermodul_) | :white_check_mark: |
| Differential Module 1 - 4 (_Differenzmodul_)| :white_check_mark: |
| Circulation 1 - 4 (_Zirkulation_)| :white_check_mark: |

## How To

### Installation

```
$ pip3 install pysolarfocus
```

### Basic Example

```python
from pysolarfocus import SolarfocusAPI,Systems,ApiVersions

# Create the Solarfocus API client
solarfocus = SolarfocusAPI(
    ip="solarfocus",                    # adapt IP-Address
    system=Systems.VAMPAIR,             # for biomass boiler change to Systems.THERMINATOR / ECOTOP
    api_version=ApiVersions.V_25_030)   # select Solarfocus version

solarfocus.connect()
# Fetch the values
solarfocus.update()

# Print the values
print(solarfocus)
print(solarfocus.heating_circuits[0])
```

Output:

```
❯ uv run example.py
--------------------------------------------------
SolarfocusAPI, v5.1.1
--------------------------------------------------
+ System: Vampair
+ Version: 25.030
--------------------------------------------------
============
HeatingCircuit
============
---Input:
supply_temperature | raw:257 scaled:25.700000000000003
room_temperature | raw:224 scaled:22.400000000000002
humidity | raw:480 scaled:48.0
limit_thermostat | raw:1 scaled:1
circulator_pump | raw:0 scaled:0
mixer_valve | raw:0 scaled:0
state | raw:0 scaled:0
---Holding:
target_supply_temperature | raw:0 scaled:0.0
cooling | raw:0 scaled:0
mode | raw:3 scaled:3
target_room_temperature | raw:0 scaled:0.0
indoor_temperature_external | raw:224 scaled:22.4
indoor_humidity_external | raw:480 scaled:48.0
heating_mode | raw:2 scaled:2


============
Boiler
============
---Input:
....
```

### Handling multiple components
Solarfocus systems allow the use of multiple heating circuits, buffers, boilers, and fresh water modules. The api can be configured to interact with multiple components.

```python
# Create the Solarfocus API client with 2 Heating Circuits
solarfocus = SolarfocusAPI(ip="[Your-IP]",heating_circuit_count=2,system=Systems.VAMPAIR)
# Connect to the heating system
solarfocus.connect()

# Update all heating circuits
solarfocus.update_heating()

# Update only the first heating circuit
solarfocus.heating_circuits[0].update()
# Print the first heating circuit
print(solarfocus.heating_circuits[0])

# Set the temperature of the first heating circuit to 30°C
solarfocus.heating_circuits[0].indoor_temperature_external.set_unscaled_value(30)
# Write the value to the heating system
solarfocus.heating_circuits[0].indoor_temperature_external.commit()
```

### Convenitently set modes
Control the heating system by setting modes using the provided classes

```python
# Without convenience method
solarfocus.heating_circuits[0].mode.set_unscaled_value(0)
solarfocus.heating_circuits[0].mode.commit()

# RECOMMENDED: Uitilizing convenience methods for modes
solarfocus.set_heating_circuit_mode(0, HeatingCircuitMode.ALWAYS_ON)
```

### API-Version specification
By default, the integration uses API-Version`21.140`. If your system is newer, you can specify
the version by using the `api_version` parameter.

```python
solarfocus = SolarfocusAPI(ip="[Your-IP]", system=Systems.VAMPAIR, api_version=ApiVersions.V_23_020)
```

You can find the API-Version displayed in the header of the screen of your Solarfocus system:

<img src="images/sf-version.png?raw=true" width="500">

## Changelog of API-Versions
> **Note**
> The API-Version of Solarfocus is independent of the versions of this library. Below list refers to
> the Solarfocus versions. See [releases](https://github.com/LavermanJJ/pysolarfocus/releases) for the changelog
> of this library.

#### 25.030
* Add differential modules
* Add circulation
* Add multiple solar modules
* Adapt for changes in registers for heat pump

#### 23.020
* Add fresh water module state.

#### 23.010
* Add biomass boiler pellet statistics.

#### 22.090
* Add biomass boiler sweep function control.
* Allow input of external buffer values.
