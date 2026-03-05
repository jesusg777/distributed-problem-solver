import json
import requests
import sys
import logging
import log
import socket
from Sockets import listen_socket, send_to_cli
from Crypter.crypter import EncryptionHandler
from problem_factory_method.creator_fibonacciVerifier import CreatorFibonacciVerifier
from problem_factory_method.creator_fizzbuzz import CreatorFizzBuzz
from problem_factory_method.creator_primeClassifier import CreatorPrimeClassifier

def process_and_send_data():
    crypter = EncryptionHandler()
    crypter.generate_keys()
    
    public_key_pem = crypter.public_key_pem.decode()
    url_key = "http://127.0.0.1:5000/public_key"
    data = {'public_key': public_key_pem}

    try:
        request = requests.post(url_key, json=data, timeout=10)
        request.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send public key: {e}")
        sys.exit()

    if request.status_code == 200:
        try:
            public_key = request.json().get('public_key')
            crypter.public_key_pem = public_key
        except (ValueError, KeyError) as e:
            logging.error(f"Failed to parse public key response: {e}")
            sys.exit()
    else:
        logging.error(f"Failed to get public key, status code: {request.status_code}")
        sys.exit()

    url_numbers = "http://127.0.0.1:5000/numbers"

    while True:
        try:
            json_data = listen_socket()
            logging.info("Received JSON data from socket: %s", json_data)
        except Exception as e:
            logging.error(f"Error listening to socket: {e}")
            continue

        if 'Kill' in json_data and json_data['Kill'] is True:
            url_shutdown = "http://127.0.0.1:5000/shutdown"
            try: 
                response = requests.get(url_shutdown)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                logging.info("Shutting down...")
                sys.exit()

        if 'Problem' in json_data:
            try:
                problem_solver = json_data['Problem']
                count = json_data['CountNumbers']
                min = json_data['MinNumber']
                max = json_data['MaxNumber']
                output_file = json_data['OutPutFile']
                output_cmd = json_data['OutPutCmd']

                data = {
                    'count': count,
                    'min': min,
                    'max': max
                }

                crypt_data = crypter.encrypt(data)

                try:
                    response = requests.post(url_numbers, json=crypt_data, timeout=10)
                    response.raise_for_status()
                    logging.info("Sent encrypted data to server")
                except requests.exceptions.RequestException as e:
                    logging.error(f"Failed to create data: {e}")
                    continue

                if response.status_code == 201:
                    try:
                        results = response.json()['encrypt_result']
                        decrypt_results = crypter.decrypt(results)
                        numbers = decrypt_results['numbers']
                    except (ValueError, KeyError) as e:
                        logging.error(f"Failed to parse or decrypt results: {e}")
                        continue

                    if numbers:
                        if problem_solver == 'FizzBuzz':
                            solver = CreatorFizzBuzz().factory_method()
                        elif problem_solver == 'FibonacciVerifier':
                            solver = CreatorFibonacciVerifier().factory_method()
                        elif problem_solver == 'PrimeClassifier':
                            solver = CreatorPrimeClassifier().factory_method()

                        results = solver.solve_problem(numbers)

                        result_data = {
                            'problem_solver': problem_solver,
                            'numbers': numbers,
                            'results': results,
                            'output_file': output_file,
                            'output_cmd': output_cmd
                        }

                        try:
                            send_to_cli(result_data)
                            logging.info("Sent results to CLI")
                        except Exception as e:
                            logging.error(f"Failed to send results to CLI: {e}")

                    else:
                        logging.warning('No data found.')
                else:
                    logging.error(f"Failed to create data, status code: {response.status_code}")
            except KeyError as e:
                logging.error(f"Missing key in JSON data: {e}")


if __name__ == "__main__":
    try:
        process_and_send_data()
    except Exception as e:
        logging.critical(f"Unhandled exception: {e}")
        sys.exit()
