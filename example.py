from pysolarfocus import ApiVersions, SolarfocusAPI, Systems

# Create the Solarfocus API client
solarfocus = SolarfocusAPI(
    ip="solarfocus", system=Systems.VAMPAIR, api_version=ApiVersions.V_23_020  # adapt IP-Address  # change to Systems.Therminator
)  # select Solarfocus version

if not solarfocus.connect():
    print("Connecting to solarfocus failed.")
    exit(1)

# Fetch the values
if not solarfocus.update():
    print("Updating solarfocus failed.")
    exit(1)

# Print the values
print(solarfocus)
print(solarfocus.heating_circuits[0])
print("\n")
print(solarfocus.boilers[0])
print("\n")
print(solarfocus.buffers[0])
print("\n")
if solarfocus.system in  [Systems.THERMINATOR, Systems.ECOTOP]:
    print(solarfocus.biomassboiler)
if solarfocus.system is Systems.VAMPAIR:
    print(solarfocus.heatpump)
print("\n")
print(solarfocus.photovoltaic)
print("\n")
print(solarfocus.fresh_water_modules[0])
print("\n")
print(solarfocus.solar)
print("\n")
