import header
import encryptions

class Client(header.NH.NetworkHandler):
    def __init__(self, ip, port):
        self.privateKey = "password"
        self.salt = "password"
        super().__init__(ip, port)
        self.knownServers = {}

        with open('ips.txt', 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                ip, port = line.split()
                pk = header.KeyReader.read_file(f"pk{i + 1}.pem")
                self.knownServers[i + 1] = {'ip': ip, 'port': port, 'pk': pk}

    def handle_received_data(self, data):
        data = encryptions.customerDecrypt(salt=self.salt,string_key=self.privateKey,encrypted_message=data)
        now = header.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(data, current_time)

    def send_message(self, filename):
        with open(filename, 'r') as file:
            messages = []
            for line in file:
                message_data = line.strip().split()
                if len(message_data) != 7:
                    print("Invalid message format")
                    continue

                message, path, round_num, password, salt, dest_ip, dest_port = message_data
                message = encryptions.customerEncrypt(salt=salt, string_key=password, message=message)#symetric - fernet
                dest_port = int(dest_port)
                path = path.split(',')

                for i in range(len(path)):
                    message = {"ip": dest_ip, "port": dest_port, "message": message}
                    message = header.map_to_string(message)
                    message = encryptions.serverEncrypt(message, self.knownServers[int(path[len(path) - 1 - i])]['pk']).decode()
                    dest_ip = self.knownServers[int(path[len(path) - 1 - i])]['ip']
                    dest_port = int(self.knownServers[int(path[len(path) - 1 - i])]['port'])
                messages.append({"ip": dest_ip, "port": dest_port, "message": message, "round": round_num})
            messages = sorted(messages, key=lambda x: x["round"])
            currRound = 0
            for message in messages:
                header.time.sleep(10*(int(message["round"]) - currRound))
                self.send_data(message['ip'], int(message['port']), message['message'])
    
    def changeKeys(self,password,salt):
        self.privateKey = password
        self.salt = salt