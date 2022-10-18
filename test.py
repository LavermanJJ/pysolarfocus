from pymodbus.client.sync import ModbusTcpClient
from pysolarfocus import SolarfocusAPI,Systems,PORT

client = ModbusTcpClient('192.168.188.63',PORT)
client.connect()
api = SolarfocusAPI(client,Systems.Therminator)

api.update_heating()

print(api.heating_circuit)