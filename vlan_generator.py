
#!/usr/bin/env python3
"""
VLAN Configuration Generator branch_b
Reads devices from inventory file and generates VLAN configs
Test line
"""
import os
import yaml
from pathlib import Path

def ensure_output_directory():
    """Create output directory if it doesn't exist"""
    # Define the output directory path
    output_dir = Path("configs")
    # Create directory if it doesn't exist (no error if it does)
    output_dir.mkdir(exist_ok=True)
    # Confirm directory is ready
    print(f"✓ Output directory ensured: {output_dir}")
    # Return the Path object for use elsewhere
    return output_dir

def load_inventory(inventory_file="inventory.yml"):
    """
    Load devices from YAML inventory file
    Expected format:
    devices:
      - name: switch1
        type: cisco_ios
      - name: router1  
        type: cisco_ios
    """
    try:
        # Open and read the YAML inventory file
        with open(inventory_file, 'r') as file:
            # Parse YAML content into Python dictionary
            inventory = yaml.safe_load(file)
        # Return devices list, or empty list if no devices key
        return inventory.get('devices', [])
    except FileNotFoundError:
        # Handle case where inventory file doesn't exist
        print(f"Error: Inventory file '{inventory_file}' not found")
        # Return empty list to avoid crashing
        return []
    except yaml.YAMLError as e:
        # Handle case where YAML syntax is invalid
        print(f"Error parsing YAML file: {e}")
        # Return empty list to avoid crashing
        return []

def generate_vlan_configurations(device_name, vlans_range=(5, 10)):
    """
    Generate VLAN configurations for a device
    Returns: List of configuration commands
    """
    # Unpack range tuple (default VLANs 5-10)
    start_vlan, end_vlan = vlans_range
    # Start with empty list for configuration commands
    configs = []
    
    # Add configuration header and enter configuration mode
    # Comment with device name
    configs.append(f"! VLAN Configuration for {device_name}")
    # Enter global configuration mode
    configs.append("configure terminal")
    
    # Generate VLAN commands for each VLAN in the range
    # +1 to include the end VLAN
    for vlan_id in range(start_vlan, end_vlan + 1):
        # Create VLAN
        configs.append(f"vlan {vlan_id}")
        # Name VLAN with 3-digit padding (e.g., VLAN_005)
        configs.append(f" name VLAN_{vlan_id:03d}")
        # Exit VLAN configuration mode
        configs.append(" exit")
    
    # Add configuration footer
    # Exit global configuration mode
    configs.append("end")
    # Save configuration to startup
    configs.append("write memory")
    # Empty line for readability in output file
    configs.append("")
    
    # Return the complete list of configuration commands
    return configs

def save_configuration(device_name, configurations, output_dir):
    """Save configurations to file"""
    # Create filename using device name (e.g., core_switch_01_vlan_config.txt)
    filename = output_dir / f"{device_name}_vlan_config.txt"
    
    # Write all configuration commands to the file, joined by newlines
    with open(filename, 'w') as file:
        # Convert list to string with newlines
        file.write('\n'.join(configurations))
    
    # Return the path where file was saved
    return filename

def print_configurations(device_name, configurations):
    """Print configurations to console"""
    # Print a visual separator and device header
    # Print line of 50 equals signs
    print(f"\n{'='*50}")
    print(f"VLAN Configurations for: {device_name}")
    print(f"{'='*50}")
    # Print each configuration line
    for line in configurations:
        print(line)

def main():
    """Main function to generate VLAN configurations"""
    print("VLAN Configuration Generator")
    print("Loading inventory...")
    
    # Ensure output directory exists before we try to save files
    output_dir = ensure_output_directory()
    
    # Load devices from inventory file
    devices = load_inventory()
    
    # Check if we found any devices
    if not devices:
        print("No devices found in inventory. Exiting.")
        # Exit early if no devices
        return
    
    print(f"Found {len(devices)} device(s) in inventory")
    
    # Process each device in the inventory
    for device in devices:
        # Get device name (e.g., "core_switch_01")
        device_name = device['name']
        # Get device type, default to cisco_ios
        device_type = device.get('type', 'cisco_ios')
        
        print(f"\nGenerating VLANs for: {device_name} ({device_type})")
        
        # Generate VLAN configurations (VLANs 5-10 by default)
        configurations = generate_vlan_configurations(device_name, (5, 10))
        
        # Print configurations to console for immediate viewing
        print_configurations(device_name, configurations)
        
        # Save configurations to file for later use
        saved_file = save_configuration(device_name, configurations, output_dir)
        print(f"Configuration saved to: {saved_file}")
    
    # Final summary
    print(f"\nVLAN configuration generation completed!")
    print(f"All files saved in: {output_dir}")

# This condition means: "Only run main() if this script is executed directly"
# (not if it's imported as a module in another script)
if __name__ == "__main__":
    main()
