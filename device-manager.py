import asyncio
import platform
import logging

from bleak import BleakScanner, BleakClient
import paramiko
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Bluetooth Functions ---

async def scan_bluetooth_devices():
    """Scans for nearby Bluetooth Low Energy devices."""
    logging.info("Scanning for BLE devices... (Ctrl+C to stop)")
    devices = await BleakScanner.discover()
    if not devices:
        logging.info("No devices found.")
        return []
    print("\nFound Devices:")
    for i, device in enumerate(devices):
        print(f"[{i+1}] {device.name} | Address: {device.address}")
    return devices

async def connect_bluetooth_device(device_address):
    """Attempts to connect to a specific BLE device."""
    try:
        async with BleakClient(device_address) as client:
            logging.info(f"Connected to {device_address}")
            # You would add code here to read/write GATT characteristics
            # For demonstration, we just stay connected briefly
            await asyncio.sleep(5.0) 
            logging.info(f"Disconnected from {device_address}")
            return True
    except Exception as e:
        logging.error(f"Failed to connect to {device_address}: {e}")
        return False

# --- SSH Functions ---
def ssh_connect_and_run(hostname, username, password=None, command="ls -la"):
    """Connects via SSH and runs a command using Paramiko."""
    client = paramiko.SSHClient()
    # Automatically add the server's host key (use with caution in production)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        logging.info(f"Attempting to connect to {hostname} via SSH...")
        client.connect(hostname, port=22, username=username, password=password, timeout=10)
        logging.info(f"Successfully connected to {hostname}.")

        logging.info(f"Executing command: '{command}'")
        stdin, stdout, stderr = client.exec_command(command)
        
        print("\n--- Command Output (STDOUT) ---")
        for line in stdout:
            print(line.strip())
        
        print("--- Errors (STDERR) ---")
        for line in stderr:
            print(line.strip())
            
    except paramiko.AuthenticationException:
      logging.error("Authentication failed. Please check username and password/keys.")
    except paramiko.SSHException as e:
        logging.error(f"SSH error: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        if client:
            client.close()
            logging.info("SSH connection closed.")
  # --- Main Interface ---

def main():
    print("Welcome to the BT-SSH Device Manager CLI Tool.")
    while True:
        print("\nSelect an option:")
        print("1. Scan for Bluetooth Devices")
        print("2. Connect via SSH and run command")
        print("3. Exit")
        choice = input("> Enter your choice: ")

        if choice == '1':
            # Use asyncio to run the async Bluetooth function
            asyncio.run(scan_bluetooth_devices())
        elif choice == '2':
            hostname = input("Enter target IP/Hostname: ")
            username = input("Enter SSH username: ")
            # In a real app, use a secure way to get passwords
            password = input("Enter SSH password (leave blank for key auth if configured): ") 
            command = input("Enter command to run (default 'ls -la'): ") or "ls -la"
            ssh_connect_and_run(hostname, username, password, command)
        elif choice == '3':
            break
        else:
          print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
