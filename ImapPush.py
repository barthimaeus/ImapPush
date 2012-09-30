import imaplib
import yaml, json
import requests
import threading

url = "https://android.googleapis.com/gcm/send"
config = None
connection = None
count = 0

def checkmail():
    global count
    _count = len(connection.search(None, 'UnSeen')[1][0].split())

    if not _count == count:
        if _count > count:
            print("%i Unread Email!" % _count)
            values = {"registration_ids": config["regid"],
                      "data": {"message": "%i Unread Email!" % _count, "sender": "Email"}}
            requests.post(url, data=json.dumps(values), headers=headers)
        count = _count

    threading.Timer(3, checkmail).start()

if __name__ == "__main__":
    with open("config.sample.yaml", "r") as f:
        config = yaml.load(f.read())

    headers = {"Content-Type": "application/json",
               "Authorization": "key=%s" % config["apikey"]}

    connection = imaplib.IMAP4(config["hostname"], config["port"])
    connection.starttls()
    connection.login(config["username"], config["password"])
    connection.select()

    checkmail()