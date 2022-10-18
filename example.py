from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pysolarfocus import SolarfocusAPI, PORT,Systems

# Create a Modbus client 
# TODO: Adapt IP-Address
client = ModbusClient("IP-Address", port=PORT) 
client.connect()

# Create the Solarfocus API client
solarfocus = SolarfocusAPI(client, Systems.Vampair)

# Fetch the values
solarfocus.update()

# Print the values
print(solarfocus.heating_circuit)
print("\n")
print(solarfocus.boiler)
print("\n")
print(solarfocus.buffer)
print("\n")
print(solarfocus.heatpump)
print("\n")
print(solarfocus.photovoltaic)
