import subprocess
import os
import validators
import sys


def main():
    clear_screen()
    print("DNS Query Tool")
    print("----------------")
    v_install = str(input("Do you wanna install the DNS query tools? (Y/N) ")).lower()
    if v_install == "y":
        check_install('dnsutils')
        check_install('curl')
        check_install('traceroute')
        check_install('whois')
        check_install('nmap')

    clear_screen()
    while True:
        # Input URL from user
        global url  # make url a global variable to access it in execute_command()
        while True:
            clear_screen()

            print("DNS Query Tool")
            print("----------------")
            url = input("Enter the URL to perform DNS query: ").strip()
            if url == "":
                clear_screen()
                sys.exit()
               
            full_url = "https://"+url      
            if is_valid_url(full_url):
                break 


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


def is_valid_url(url):
    return validators.url(url)


def get_dns_records(url):
    """Perform a 'dig' query on the provided URL."""
    return subprocess.run(['dig', '+short', url], capture_output=True, text=True)


def execute_command(url):
    while True:
        clear_screen()
        print("Execute the specified command in a Linux terminal")
        print("\nAvailable commands:")
        print("1. nslookup - Display NS records")
        print("2. host - Display host information")
        print("3. dig - Display A records (IP addresses)")
        print("4. curl - Fetches content from a URL")
        print("5. traceroute - Trace route to a host")
        print("6. whois - Display WHOIS information")
        print("7. nmap - Port scanning")

        choice = input("\nSelect a command to execute: ")

        if choice == "1":
            f_nslookup(url)
        elif choice == "2":
            subprocess.run(['host', url], check=True)
        elif choice == "3":
            subprocess.run(['dig', url], check=True)
        elif choice == "4":
            subprocess.run(['curl', url], check=True)
        elif choice == "5":
            subprocess.run(['traceroute', url], check=True)
        elif choice == "6":
            strip_www = url.lstrip("www.")
            subprocess.run(['whois', strip_www], check=True)
        elif choice == "7":
            subprocess.run(['nmap', url], check=True)
        else:
            return            
        

def f_nslookup(url):
    while True:
        clear_screen()
        print("Execute the specified nslookup command")
        print("\nAvailable commands:")
        print("1. Basic Query")
        print("2. MX Record Query ")
        print("3. NS Record Query")
        print("4. SOA Record Query")
        print("5. TXT Record Query ")

        choice = input("\nSelect a command to execute: ")

        clear_screen()

        if choice == "1":
            subprocess.run(['nslookup', url], check=True)
        elif choice == "2":
            subprocess.run(['nslookup', '-type=MX', url], check=True)
        elif choice == "3":
            subprocess.run(['nslookup', '-type=NS', url], check=True)
        elif choice == "4":
            subprocess.run(['nslookup', '-type=SOA', url], check=True)
        elif choice == "5":
            subprocess.run(['nslookup', '-type=TXT', url], check=True)
        else:
            return
        input()




def clear_screen() ->None:
    """Clear the terminal screen."""
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")


def check_install(package):
    result = subprocess.run(['apt', 'policy', package], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(result.stdout)
    if 'install ok installed' in result.stdout:
        print(f"{package} is already installed.")
    else:
        print(f"{package} is not installed. Installing...")
        subprocess.run(['sudo', 'apt-get', 'install', '-y', package], check=True)


if __name__ == "__main__":
    main()
