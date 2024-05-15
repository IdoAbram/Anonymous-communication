import Server

server = Server.EncryptionServer('192.168.1.116', 9002, 3)
server.run()