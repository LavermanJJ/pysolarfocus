from pysolarfocus import SolarfocusAPI, PORT,Systems

# Create the Solarfocus API client
# TODO: Adapt IP-Address
solarfocus = SolarfocusAPI(ip="10.10.10.237", heating_circuit_count=0, system=Systems.Vampair)
solarfocus.connect()
# Fetch the values
solarfocus.update()



# Print the values
#print(solarfocus.heating_circuit)
print("\n")
print(solarfocus.heating_circuits[0])
print("\n")
#print(solarfocus.buffer)
#print("\n")
#print(solarfocus.heatpump)
#print("\n")
#print(solarfocus.photovoltaic)
#