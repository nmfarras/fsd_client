# utility.py

# def send_message(connection, message):
    # try:
        # connection.sendall(message.encode())
    # except Exception as e:
        # print(f"Error sending message: {e}")
        

# Emergency flags
emergency_flags = {
    'LGR': 1,
    'RGR': 2,
    'NGR': 4,
    'LGC': 16,
    'RGC': 32,
    'NGC': 64,
    'E1S': 256,
    'E2S': 512,
    'E3S': 1024,
    'E4S': 2048,
    'E1F': 4096,
    'E2F': 8192,
    'E3F': 16384,
    'E4F': 32768
}

# Light flags
light_flags = {
    'BCN': 2,
    'STR': 4,
    'NAV': 8,
    'LND': 32,
    'TAX': 64,
    'WNG': 256,
    'EMG': 2048
}

def check_active_emergency_flags(flag_value):
    return [flag for flag, value in emergency_flags.items() if flag_value & value]

# # Example usage for emergency flags
# combined_emergency_flag_value = 4352
# active_emergency_flags = check_active_emergency_flags(combined_emergency_flag_value)
# print("Active emergency flags:", active_emergency_flags)

def check_active_light_flags(flag_value):
    return [flag for flag, value in light_flags.items() if flag_value & value]

# # Example usage for light flags
# combined_light_flag_value = 72
# active_light_flags = check_active_light_flags(combined_light_flag_value)
# print("Active light flags:", active_light_flags)
