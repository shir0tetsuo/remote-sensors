import os
import subprocess

UUID = "aa45f871-0dfd-4dba-a0e8-c835ff216faa"  # Replace with your network's UUID

def is_connected():
    """Check if the Raspberry Pi is connected to a network."""
    try:
        # Get the current network SSID using iwgetid
        output = subprocess.check_output(["iwgetid", "--raw"], stderr=subprocess.DEVNULL)
        return bool(output.strip())
    except subprocess.CalledProcessError:
        return False

def reconnect():
    """Reconnect to the network using the UUID."""
    print("Connection lost. Attempting to reconnect...")
    os.system(f"sudo nmcli connection up uuid {UUID}")

if __name__ == "__main__":
    if not is_connected():
        reconnect()
    else:
        print("Network is connected.")
