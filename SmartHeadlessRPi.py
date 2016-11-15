sys,socket, fcntl, struct, socket, array,os
from time import sleep
from twython import Twython

Device_Name="Your Device Name"
time.sleep(30)


#get IP address
def get_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915,
                struct.pack('256s', ifname[:15])

                )[20:24])

IP_address = get_ip('wlan0')

#get ESSID
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
maxLength = {
    "interface": 16,
    "essid": 32
}
calls = {
    "SIOCGIWESSID": 0x8B1B
}

def getESSID(interface):
    """Return the ESSID for an interface, or None if we aren't connected."""
    essid = array.array("c", "\0" * maxLength["essid"])
    essidPointer, essidLength = essid.buffer_info()
    request = array.array("c",
        interface.ljust(maxLength["interface"], "\0") +
        struct.pack("PHH", essidPointer, essidLength, 0)
    )
    fcntl.ioctl(sock.fileno(), calls["SIOCGIWESSID"], request)
name = essid.tostring().rstrip("\0")
    if name:
        return name
    return None

essid = getESSID('wlan0')

tweetStr = "Device Name: "+Device_Name + " IP Address: " + IP_address + " ESSID: " + essid
print tweetStr

apiKey = '[Your Api Key]'
apiSecret = '[Your Api secret]'
accessToken = '[Your access token]'
accessTokenSecret = '[Your access token secret]'

api = Twython(apiKey, apiSecret, accessToken, accessTokenSecret)

api.send_direct_message(user_id='Your User ID',text=tweetStr)
