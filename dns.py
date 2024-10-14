import subprocess
import os


def main():
    clear_screen()

    print("DNS Query Tool")
    print("----------------")

    # Input URL from user
    global url  # make url a global variable to access it in execute_command()
    url = input("Enter the URL to perform DNS query: ")

    # Perform dig query and display output
    records = get_dns_records(url)
    if records.returncode == 0:
        print("\nDig Query Output:")
        for line in str(records.stdout).splitlines():
            print(line)
    else:
        print(f"\nError performing 'dig' query on {url}:")
        print(str(records.stderr))

    execute_command(url)


def get_dns_records(url):
    """Perform a 'dig' query on the provided URL."""
    return subprocess.run(['dig', '+short', url], capture_output=True, text=True)

def execute_command(url):
    """Execute the specified command in a Linux terminal."""
    print("\nAvailable commands:")
    print("1. nslookup - Display NS records")
    print("2. host - Display host information")
    print("3. dig - Display A records (IP addresses)")
    print("4. ping - Test connectivity to a host")
    print("5. curl - Fetches content from a URL")
    print("6. traceroute - Trace route to a host")
    print("7. whois - Display WHOIS information")
    print("8. nmap - Port scanning")

    choice = input("\nSelect a command to execute: ")

    if choice == "1":
        subprocess.run(['nslookup', url], check=True)
    elif choice == "2":
        subprocess.run(['host', url], check=True)
    elif choice == "3":
        subprocess.run(['dig', url], check=True)
    elif choice == "4":
        subprocess.run(['ping', url], check=True)
    elif choice == "5":
        subprocess.run(['curl', url], check=True)
    elif choice == "6":
        subprocess.run(['traceroute', url], check=True)
    elif choice == "7":
        subprocess.run(['whois', url], check=True)
    elif choice == "8":
        subprocess.run(['nmap', url], check=True)
    else:
        print("\nExiting...")



def clear_screen() ->None:
    """Clear the terminal screen."""

    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")
    return



if __name__ == "__main__":
    main()