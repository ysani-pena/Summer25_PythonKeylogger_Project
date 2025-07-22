import os
import smtplib
import getpass
import socket
from email.message import EmailMessage

# Purpose:
#This script acts as a safety net to catch any keywords that weren't reported during active monitoring (like when a student types a #keyword right before logging off). It runs automatically when a user logs off.


# --- CONFIG (matches main script) ---
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

BUFFER_PATH = os.path.join(os.environ['LOCALAPPDATA'], 'Keylogger', 'buffer.txt') #points to same buffer file location
CONTEXT_CHARS = 15  # Characters before/after to include

# Email settings (same as main script)
ALERT_EMAIL = 'fletcherit@fletcheracademy.org'
SENDER_EMAIL = 'ypena@fletcheracademy.org'
SENDER_PASSWORD = 'zfme dbpb crhd bjdk'

username = getpass.getuser()
hostname = socket.gethostname()

# --- SIMPLE CHECKER ---
def check_buffer():
    #this will immediately exit if no typing history exists in the buffer
    if not os.path.exists(BUFFER_PATH):
        return
   
   #opens buffer file in read/write mode and converts all text to lowercase for case-insensitve matching
    with open(BUFFER_PATH, 'r+') as f:
        text = f.read().lower()
       
        # Checks for ANY keyword from KEYWORD dictionary
        for variation, main_keyword in KEYWORD_MAP.items():
            if variation in text:
                index = text.find(variation)
                 #grabs characters (15) before and after keyword and adjusts for text boundaries
                start = max(0, index - CONTEXT_CHARS)
                end = index + len(variation) + CONTEXT_CHARS
                context = text[start:end]
               
                send_alert(main_keyword, context) #sends the email with keyword
               
                # Clears ONLY the reported part and preserves any unreported text
                f.seek(0)
                remaining = text[end:]
                f.write(remaining)
                f.truncate()
                break

def send_alert(keyword, context):
    msg = EmailMessage()
    msg['Subject'] = f"ALERT: Keyword '{keyword}' typed by {username} at logoff"
    msg['From'] = SENDER_EMAIL
    msg['To'] = ALERT_EMAIL
    msg.set_content(
        f"Keyword Detected: '{keyword}'\n"
        f"User: {username}\n"
        f"Computer: {hostname}\n"
        f"Context detected at logoff: {context}\n"     
    )
   
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
        smtp.send_message(msg)

#this is what will run the program auto when called from GPO logoff script or manually executed
if __name__ == "__main__":
    check_buffer()