package util

import (
	"fmt"
	"net"
)

func ConnectToServer(address string) (net.Conn, error) {
	conn, err := net.Dial("tcp", address)
	if err != nil {
		return nil, fmt.Errorf("error connecting to server: %v", err)
	}
	return conn, nil
}

func SendData(data []byte, connection net.Conn) error {
	_, err := connection.Write(data)
	if err != nil {
		return fmt.Errorf("error sending data: %v", err)
	}
	fmt.Println("Data sent to server:", string(data))
	return nil
}

func ReceiveData(socketPort string) (net.Conn, error) {
	reader, err := net.Listen("tcp", socketPort)

	if err != nil {
		return nil, err
	}

	conn, err := reader.Accept()
	if err != nil {
		return nil, err
	}
	return conn, nil
}
