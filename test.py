from pymodbus.client import ModbusTcpClient as ModbusClient
from pysolarfocus import SolarfocusAPI,Systems,PORT

client = ModbusClient("192.168.188.63", port=PORT)
client.connect()

solarfocus = SolarfocusAPI(client,Systems.Therminator)

solarfocus.update()

print(solarfocus.buffer)
print(solarfocus.pelletsboiler)
print(solarfocus.heating_circuit)