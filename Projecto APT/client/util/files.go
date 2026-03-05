package util

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func Write(hashedPassword string) {
	file, err := os.OpenFile("files/password.txt", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Println("error creating or opening file:", err)
		return
	}
	defer file.Close()

	_, err = fmt.Fprintf(file, "%s\n", hashedPassword)
	if err != nil {
		fmt.Println("error writing to the file:", err)
		return
	}
}

func Read() string {
	file, err := os.Open("files/password.txt")
	if err != nil {
		fmt.Println("error opening the file:", err)
		return ""
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	scanner.Scan()
	return scanner.Text()
}

func WriteResultToFile(numbers []int, results []string, problem string) {
	file, err := os.Create("files/results.txt")
	if err != nil {
		fmt.Println("Error creating file:", err)
		return
	}
	defer file.Close()

	writer := bufio.NewWriter(file)
	writer.WriteString("Problem to solve: " + problem + "\n")
	for i := 0; i < len(numbers); i++ {
		str := strconv.Itoa(numbers[i])
		writer.WriteString(str + " " + results[i] + "\n")
	}
	writer.Flush()
}
