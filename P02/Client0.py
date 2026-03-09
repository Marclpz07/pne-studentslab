import socket
class Client:
    """Class for sending messages to a server"""

    def __init__(self, ip, port):
        """
        Initialize the Client with IP and PORT

        Args:
            ip (str): Server IP address
            port (int): Server port number
        """
        self.ip = ip
        self.port = port

    def ping(self):
        """
        Send a ping message to the server and return the server info"""
        print("OK!")

    def __str__(self):
        return f"Conection to SERVER at {self.ip}, port: {self.port}"

    def talk(self, msg):
        # -- Create the socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # establish the connection to the Server (IP, PORT)
        s.connect((self.ip, self.port))

        # Send data.
        s.send(str.encode(msg))

        # Receive data
        response = s.recv(2048).decode("utf-8")

        # Close the socket
        s.close()

        # Return the response
        return response