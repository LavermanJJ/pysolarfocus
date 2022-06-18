import argparse
import pysolarfocus as sf

from pymodbus.client.sync import ModbusTcpClient as ModbusClient

from pysolarfocus.const import PORT


def run(host):
    client =  ModbusClient(host="172.16.1.17", port=PORT)
    client.connect()

    solarfocus = sf.SolarfocusAPI(client)
    #solarfocus.update()

    #if solarfocus.update_heating():
    #    print(f"vorlauf: {solarfocus.hc1_target_temperatur}")

    solarfocus.smart_grid_request_operation(False)

    #solarfocus.set_smart_grid(4)
    #print(f"{solarfocus._heating_circuit_holding_regs}")

    #print(f"vorlauf: {solarfocus.hc1_state}")

    #attrs = vars(solarfocus)
    #print(', '.join("%s: %s" % item for item in attrs.items()))

    #value=solarfocus.hc1_supply_temp
    #print(f"vorlauf: {solarfocus.hc1_state}")


def main():
    parser = argparse.ArgumentParser(description="Solarfocus Heating System")
    parser.add_argument("--host", help="Local Solarfocus host (or IP)")
    args = parser.parse_args()

    run(args.host)


if __name__ == "__main__":
    main()