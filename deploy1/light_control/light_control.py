import bluetooth


def light_opening():
    bd_addr = "12:29:4b:0f:31:8b"
    port = 1

    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bd_addr, port))

    sock.send("1")

    data = sock.recv(1024)

    sock.close()


def light_close():
    bd_addr = "12:29:4b:0f:31:8b"
    port = 1
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bd_addr, port))
    sock.send("2")
    data = sock.recv(1024)
    sock.close()

#if __name__ == "__main__":
#	light_close()
