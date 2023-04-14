from pysolarfocus import SolarfocusAPI,Systems,ApiVersions

# Create the Solarfocus API client
solarfocus = SolarfocusAPI(
    ip="solarfocus",                    # adapt IP-Address 
    system=Systems.Vampair,             # change to Systems.Therminator
    api_version=ApiVersions.V_23_020)   # select Solarfocus version

solarfocus.connect()
# Fetch the values
solarfocus.update()

# Print the values
print(solarfocus)
print(solarfocus.heating_circuits[0])
print("\n")
print(solarfocus.boilers[0])
print("\n")
print(solarfocus.buffers[0])
print("\n")
if solarfocus.system is Systems.Therminator:
    print(solarfocus.pelletsboiler)
if solarfocus.system is Systems.Vampair:
    print(solarfocus.heatpump)
print("\n")
print(solarfocus.photovoltaic)
print("\n")
print(solarfocus.solar)
print("\n")