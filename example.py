from pysolarfocus import SolarfocusAPI, Systems

# Create the Solarfocus API client
# TODO: Adapt IP-Address
solarfocus = SolarfocusAPI(ip="IP-Address", system=Systems.Vampair)
solarfocus.connect()

# Fetch the values
solarfocus.update()

# Print the values
print(solarfocus.heating_circuit)
print("\n")
print(solarfocus.boiler)
print("\n")
print(solarfocus.buffer)
print("\n")

if solarfocus.system == Systems.Vampair:
    print(solarfocus.heatpump)
else:
    print(solarfocus.pelletsboiler)
    
print("\n")
print(solarfocus.photovoltaic)
print("\n")
print(solarfocus.solar)
