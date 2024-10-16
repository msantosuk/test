import subprocess
import os
import validators
import sys
import time


def main():
    clear_screen()
    print(" \n DNS Query Tool")
    print(" ----------------")
    v_install = str(input(" Do you wanna install the DNS query tools? (Y/N) ")).lower()
    if v_install == "y":
        subprocess.run(['sudo','apt-get', 'update'], check=True)
        check_install('dnsutils')
        check_install('curl')
        check_install('traceroute')
        check_install('whois')
        check_install('nmap')
    main_input()

def main_input():
    clear_screen()
    while True:
        # Input URL from user
        global url  # make url a global variable to access it in execute_command()
        while True:
            clear_screen()

            print(" \n DNS Query Tool")
            print(" ----------------")
            url = input(" Enter the URL to perform DNS query: ").strip()
            if url == "":
                clear_screen()
                sys.exit()
            try:
                subprocess.run(['host', url], check=True)
            except subprocess.CalledProcessError as e:
                if e.returncode > 0:
                    print("\n< Invalid URL! >")
                    time.sleep(2)
                    continue
               
            full_url = "https://"+url      
            if is_valid_url(full_url):
                break 

        main_options(url)


def is_valid_url(url):
    return validators.url(url)


def get_dns_records(url):
    """Perform a 'dig' query on the provided URL."""
    return subprocess.run(['dig', '+short', url], capture_output=True, text=True)


def main_options(url):
    while True:
        clear_screen()
        print(" Execute the specified command in a Linux terminal")
        print(" URL: ", url)
        print(" \n Available commands:\n")
        print(" 1 - nslookup")
        print(" 2 - host")
        print(" 3 - dig")
        print(" 4 - curl")
        print(" 5 - traceroute")
        print(" 6 - whois")
        print(" 7 - nmap")

        choice = input("\n Select a command to execute: ")

        if choice == "1":
            f_nslookup(url)
        elif choice == "2":
            f_host(url)
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
        print(" Execute the specified nslookup command")
        print(" URL: ", url)
        print("\n Available commands:\n")
        print(" 1 - Find out the BASIC A record of the domain.")
        print(" 2 - Find out the MX records responsible for the email exchange.")
        print(" 3 - Find out the NS records of the domain")
        print(" 4 - Find out the SOA record of the domain.")
        print(" 5 - Find out the TXT record of the domain.")
        print(" 6 - Find out the available ANY DNS records of the domain.")
        print(" 7 - Find out the Available INFO DNS records of the domain.")
        print(" 8 - Changing the timeout interval for a reply.")
        print(" 9 - Debug mode.")

        choice = input("\n Select a command to execute: ")
        clear_screen()
        print("\n")
        try:
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
            elif choice == "6":
                subprocess.run(['nslookup', '-type=ANY', url], check=True)
            elif choice == "7":
                subprocess.run(['nslookup', '-type=hinfo', url], check=True)
            elif choice == "8":
                value = str(input(" Add the timeout time in seconds: ") or "1").strip()
                subprocess.run(['nslookup', 'f("-timeout={value}', url], check=True)            
            elif choice == "9":
                subprocess.run(['nslookup', '-debug', url], check=True)
            else:
                return
            input(" < Press enter to continue... >") 
        except subprocess.CalledProcessError as e:
            input(" < Press enter to continue... >")



def f_host(url):
    while True:
        clear_screen()
        print(" Execute the specified host command")
        print(" URL: ", url)
        print("\n Available commands:\n")
        print(" 1 - Basic - Find the A record of the domain.")
        print(" 2 - Find out the domain name servers use the -t option.")
        print(" 3 - Find out the domain CNAME,")
        print(" 4 - Find out the MX records for the domain.")
        print(" 5 - Find out the TXT records for the domain.")
        print(" 6 - Find out the Domain SOA Record.")
        print(" 7 - Find all Information of Domain Records and Zones.")
        print(" 8 - Find out domain TTL information.")
        print(" 9 - Set UDP Retries for a Lookup.")
        print(" 10 - Set Query Time Wait for Reply")        
        
        choice = input("\n Select a command to execute: ")
        clear_screen()
        print("\n")

        if choice == "1":
            subprocess.run(['host', url], check=True)
        elif choice == "2":
            subprocess.run(['host', '-t', 'ns', url], check=True)
        elif choice == "3":
            subprocess.run(['host', '-t', 'cname', url], check=True)
        elif choice == "4":
            subprocess.run(['host', '-n', '-t', 'mx', url], check=True)
        elif choice == "5":
            subprocess.run(['host', '-t', 'txt', url], check=True)
        elif choice == "6":
            strip_www = url.lstrip("www.")
            subprocess.run(['host', '-C', strip_www], check=True)
        elif choice == "7":
            subprocess.run(['host', '-a', url], check=True)
        elif choice == "8":
            subprocess.run(['host', '-v', '-t', 'a', url], check=True)
        elif choice == "9":            
            value = str(input(" Add the number of UDP tries: ") or "1").strip()
            subprocess.run(['host', '-R', value, url], check=True)
        elif choice == "10":
            value = str(input(" Add the specified time in seconds: ") or "1").strip()
            subprocess.run(['host', '-T', '-W', value, url], check=True)
        else:
            return
        input("\n\n < Press enter to continue... >")





def clear_screen() ->None:

    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")
    print("\n")


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
