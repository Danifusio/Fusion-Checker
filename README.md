# Fusion-Checker
Fusion Checker is  a minecraft account checker with many captures such as Minecraft, Gamepass and 2FA

# Instructions

Instructions for Using the Program

### 1. Clone the Repository
   
Download the code from GitHub by running the following command in your terminal:
bashgit clone https://github.com/your-username/your-repository.git
Or click "Code" and download the ZIP manually if preferred.
Install Dependencies
Ensure you have Python 3.x installed. Then, install the required libraries with:
pip install -r requirements.txt

### 2.  Configure the Program

Create a results folder in the project directory if it doesn’t exist.
Optional: Create a config.ini file in the root directory to enable webhook notifications (example):
text[Webhook]
enabled = true
url = https://your-webhook-url

### 3.Prepare a combo file (format email:password, one per line) and a proxy file (if using proxies, format ip:port or ip:port:user:password).


Run the Program
Navigate to the project directory and execute:
bashpython checker.py

Follow the console prompts:

Enter the number of threads (1-100, recommended 3-5).
Select proxy type (1: HTTP, 2: SOCKS4, 3: SOCKS5, 4: None).
Confirm if you have a webhook and provide it if needed.
Select the combo and proxy files (if applicable) using the file explorer.



### Capture files
Review the Results
Results will be saved in the results/[combo-file-name] folder in files such as:

hits.txt: Valid accounts with no specific products.
minecraft.txt: Accounts with Minecraft.
gamepass.txt: Accounts with Xbox Game Pass.
ultimate.txt: Accounts with Xbox Game Pass Ultimate.
bedrock.txt: Accounts with Minecraft Bedrock.
dungeons.txt: Accounts with Minecraft Dungeons.
legends.txt: Accounts with Minecraft Legends.
2fa.txt: Accounts with two-factor authentication.
bad.txt: Invalid accounts.
capture.txt: Additional details for valid accounts.


### Important Notes

Use proxies if checking many accounts to avoid rate limits (429).
Do not modify the code unless you understand its functionality, as it may break the program.
Press Enter when finished to close the program.

# Captures:
xbox game pass/xbox game pass ultimate accounts
minecraft capes
optifine cape
email access
last name change
hypixel rank, level, first/last login, bedwars stars, skyblock coins, ban status
