import obd

connection = obd.OBD(fast=False)

if not connection.is_connected():
    print("No OBD-II connection.")
    exit()

CMD_IAT = obd.commands.INTAKE_TEMP
CMD_VOLT = obd.commands.CONTROL_MODULE_VOLTAGE

iat = connection.query(CMD_IAT)
volt = connection.query(CMD_VOLT)

# Safe checks
if not iat.is_null():
    print("Intake Air Temp:", iat.value)
else:
    print("Intake Air Temp: N/A")

if not volt.is_null():
    print("Battery Voltage:", volt.value)
else:
    print("Battery Voltage: N/A")
