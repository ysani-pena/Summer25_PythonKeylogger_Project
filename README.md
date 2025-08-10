# Academy Keywatcher

A cross-platform, context-aware keylogger and alerting system for school-wide deployment on Windows and Chromebooks.

---

## 📋 Overview

**Academy Keywatcher** monitors keystrokes in real time, detects sensitive or high-risk keywords (with typo tolerance), captures configurable context before/after each hit, and sends immediate email alerts to the IT team. It persists only flagged data and automatically clears buffers after reporting, ensuring student privacy and compliance.

---

## 🚀 Features

- **Keyword matching** against a customizable variant→canonical map  
- **Context capture**: configurable characters before & after each flagged term  
- **Session persistence**: per-user buffer survives logoff/logon, auto-cleared on alert  
- **Email alerts** via Gmail SMTP (includes user, hostname, timestamp, context)  
- **Windows deployment**: GPO startup for `keylogger.py` + logoff sweep via `logoff_checker.py`  
- **Privacy-first**: only the small context snippet is stored/emailed, all buffers auto-purged  

---

## ⚙️ Requirements

- **Windows clients**: Python 3.13.5+ installed (bundled with GPO wrapper), network access to SMTP  
- **Email**: Gmail account with App-Password enabled  

---

# 🔧 Network & Firewall Considerations
- If your organization enforces outbound firewall rules, be sure to allow:
  - ICMP (Ping) – for basic connectivity checks (used by your BAT‐wrapper to verify reachability).
  - HTTPS (TCP 443) – so pip install keyboard in your launch script can successfully reach the PyPI servers.
  - SMTPS (TCP 465) – so keywatcher_phaseone.py can authenticate and send alert emails via Gmail’s secure SMTP endpoint.

---

## 📦 Installation & Deployment

### Windows via GPO

1. **Place** `keylogger.py` and `logoff_checker.py` in a secure network share (e.g. `\\DC01\Scripts\Keywatcher\`).  
2. **Create** a logon script (`launch_keywatcher.bat`) that:  
   - Locates `python.exe`  
   - Ensures the `keyboard` module is installed (`python -m pip install --user keyboard`)  
   - Launches `keylogger.py` with `start /b`.  
3. **Configure** Group Policy → User Configuration → Windows Settings → Scripts:  
   - **Logon** → point to `launch_keywatcher.bat`  
   - **Logoff** → point to a wrapper for `logoff_checker.py`  
4. **Update GPO**: `gpupdate /force` and verify `keywatcher_phaseone.py` runs in Task Manager.


---

## 🔧 Configuration

All keyword variants live in `KEYWORD_MAP` (both Python scripts and `content.js`).  
Adjust in-code constants:  
```python
CONTEXT_CHARS = 10
BUFFER_PERSIST_LIMIT = 30
PENDING_CHARS_NEEDED = 10
