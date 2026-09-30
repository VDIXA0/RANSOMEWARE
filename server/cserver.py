from flask import Flask, request
import sqlite3
import urllib

app = Flask(__name__)

@app.route("/save_keys", methods=["POST"])
def save_keys():
    if request.method == "POST":
        mac_address = urllib.parse.unquote(request.form.get("mac_address"))
        enc_key = urllib.parse.unquote(request.form.get("enc_key"))
        xor_key = urllib.parse.unquote(request.form.get("xor_key"))
        iv = urllib.parse.unquote(request.form.get("iv"))

        con = sqlite3.connect("keys.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS keys (mac_address TEXT, enc_key TEXT, xor_key TEXT, iv TEXT)")
        cur.execute("INSERT INTO keys (mac_address, enc_key, xor_key, iv) VALUES (?, ?, ?, ?)", (mac_address, enc_key, xor_key, iv))
        con.commit()
        con.close()
    return ""

@app.route("/get_keys", methods=["GET"])
def get_keys():
    if request.method == "GET":
        mac_address = urllib.parse.unquote(request.args.get("mac_address"))
        con = sqlite3.connect("keys.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM keys WHERE mac_address = ?", (mac_address,))
        keys = cur.fetchone()

        if keys:
            return "|".join([keys["enc_key"], keys["xor_key"], keys["iv"]])
        return ""

if __name__ == '__main__':
    host_ip = input("Enter the server host IP address (default: 0.0.0.0): ") or "0.0.0.0"
    port = int(input("Enter the server port (default: 5000): ") or 5000)

    app.run(debug=False, host=host_ip, port=port)
