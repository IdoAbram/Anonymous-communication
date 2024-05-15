import Client

client = Client.Client('127.0.0.1', 7000)
client.send_message('messages2.txt')
