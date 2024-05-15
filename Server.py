import header
import encryptions

class EncryptionServer(header.NH.NetworkHandler):
    def __init__(self, ip, port, serial_number):
        self.waitingMessages = []
        self.lock = header.threading.Lock()
        super().__init__(ip, port)
        self.sk = header.KeyReader.read_file(f"sk{serial_number}.pem")
        
    def handle_received_data(self, data):
        message = header.string_to_map(self.decrypt_message(data))
        with self.lock:
            self.waitingMessages.append(header.map_to_string(message))

    def decrypt_message(self, data):
        return encryptions.serverDecrypt(data,self.sk)

    def _process_messages(self):
        with self.lock:
            keys_to_remove = []
            header.random.shuffle(self.waitingMessages)
            for message in self.waitingMessages:
                keys_to_remove.append(message)
                message = header.string_to_map(message)
                self.send_data(message['ip'], int(message['port']), header.map_to_string(message['message']))
            self.waitingMessages = []
        header.threading.Timer(10, self._process_messages).start()

    def run(self):
        listen_thread = header.threading.Thread(target=self.listen)
        process_thread = header.threading.Thread(target=self._process_messages)

        listen_thread.start()
        process_thread.start()