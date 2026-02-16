def get_table_gcode():
    gcode = [
        "G21", 
        "G90",
        "G1 Z5 F500",
        "G1 X10 Y10 F2000",
        "M3 S1000",
        "G1 X60 Y10",
        "G1 X60 Y40",
        "G1 X10 Y40",
        "G1 X10 Y10",
        "M5",
        "G1 Z5"
    ]
    return gcode

def simulate_hardware_execution():
    commands = get_table_gcode()
    for cmd in commands:
        print(f"Hardware Logic: {cmd}")
