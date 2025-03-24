import os
import hashlib
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Function to generate a unique device ID
def get_unique_device_id():
    try:
        # Fetch ANDROID_ID
        android_id = os.popen("settings get secure android_id").read().strip()

        # Fetch Board, Model, Manufacturer
        board = os.popen("getprop ro.product.board").read().strip()
        model = os.popen("getprop ro.product.model").read().strip()
        manufacturer = os.popen("getprop ro.product.manufacturer").read().strip()

        # Combine and generate a unique hash
        raw_id = f"{android_id}-{board}-{model}-{manufacturer}"
        unique_id = hashlib.sha256(raw_id.encode()).hexdigest()

        return unique_id

    except Exception as e:
        return f"Error: {str(e)}"

# Function to verify the device ID
def verify_device(input_id):
    current_id = get_unique_device_id()
    if current_id == input_id:
        print(Fore.GREEN + Style.BRIGHT + "\n✅ Device Verified: This is the correct device.")
    else:
        print(Fore.RED + Style.BRIGHT + "\n❌ Device Mismatch: This is NOT the registered device.")

# Function to display the menu
def display_menu():
    print(Fore.CYAN + Style.BRIGHT + "=" * 40)
    print(Fore.YELLOW + Style.BRIGHT + "  UNIQUE DEVICE ID VERIFICATION TOOL")
    print(Fore.CYAN + Style.BRIGHT + "=" * 40)
    print(Fore.GREEN + Style.BRIGHT + "1. Generate ID")
    print(Fore.BLUE + Style.BRIGHT + "2. Verify ID")
    print(Fore.RED + Style.BRIGHT + "3. Exit")
    print(Fore.CYAN + Style.BRIGHT + "=" * 40)

# Main program
def main():
    while True:
        display_menu()
        choice = input(Fore.MAGENTA + Style.BRIGHT + "Enter your choice (1/2/3): ").strip()

        if choice == "1":
            unique_id = get_unique_device_id()
            print(Fore.GREEN + Style.BRIGHT + "\nYour Unique Device ID is:")
            print(Fore.YELLOW + Style.BRIGHT + unique_id)
            input(Fore.CYAN + Style.BRIGHT + "\nPress Enter to continue...")

        elif choice == "2":
            input_id = input(Fore.MAGENTA + Style.BRIGHT + "Enter the Hardware ID to verify: ").strip()
            verify_device(input_id)
            input(Fore.CYAN + Style.BRIGHT + "\nPress Enter to continue...")

        elif choice == "3":
            print(Fore.RED + Style.BRIGHT + "\nExiting the program. Goodbye! 👋")
            break

        else:
            print(Fore.RED + Style.BRIGHT + "\nInvalid choice! Please select 1, 2, or 3.")
            input(Fore.CYAN + Style.BRIGHT + "\nPress Enter to continue...")

if __name__ == "__main__":
    main()
