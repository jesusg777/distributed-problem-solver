from flask import Flask, request, jsonify
from distributions.normal_distribution import NormalDistribution
from distributions.uniform_distributuion import UniformDistribution
from crypter.crypter import EncryptionHandler
import random, os, signal

class MyApp:
    def __init__(self):
        self.app =  Flask(__name__)
        self.crypter = EncryptionHandler()
        self.crypter.generate_keys()
        
        @self.app.route('/public_key', methods=['POST'])
        def public_keys_change():
            data = request.get_json()
            if 'public_key' in data:
                public_key = self.crypter.public_key_pem.decode()
                self.crypter.public_key_pem = data['public_key'].encode()
            
                data = {'public_key': public_key}
                return jsonify(data), 200

        @self.app.route('/numbers', methods=['POST'])
        def generate_numbers():
            data = request.get_json()

            if not data:
                return jsonify({'error': 'no data'}) 
            try:
                decrypt_data = self.crypter.decrypt(data)       
            except ValueError as e:
                return jsonify({'error': 'Decryption failed'}), 500
            
            min = int(decrypt_data['min'])
            max = int(decrypt_data['max'])
            count = int(decrypt_data['count'])

            option = random.choice(['normal', 'uniform'])
            if option == 'normal':
                numbers, distribution = NormalDistribution().generate_numbers(min, max, count)
                
            if option == 'uniform':
                numbers, distribution = UniformDistribution().generate_numbers(min, max, count)
            
            result = {
                'numbers': numbers,
                'distribution': distribution
            }
            try:
                encrypt_result = self.crypter.encrypt(result)
                return jsonify({'encrypt_result': encrypt_result}), 201
            except ValueError as e:
                return jsonify({'error': 'Encryption failed', 'message': str(e)}), 500
            
        @self.app.route('/shutdown', methods=['GET'])
        def shutdown():
            print("Shutting down the server flask")
            pid = os.getpid()
            os.kill(pid, signal.SIGINT)
        

    def run_app(self):
        self.app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':  
    app = MyApp()
    app.run_app()
