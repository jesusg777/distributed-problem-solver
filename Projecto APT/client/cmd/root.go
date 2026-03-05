package cmd

import (
	"bytes"
	"cliente_project/util"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"os"

	"github.com/spf13/cobra"
)

type Data struct {
	Problem      string
	MinNumber    int64
	MaxNumber    int64
	CountNumbers int64
	OutPutFile   bool
	OutPutCmd    bool
	Kill         bool
}

type Result struct {
	Numbers []int
	Results []string
}

var problem string
var minNumber int64
var maxNumber int64
var countNumbers int64
var outPutFile bool
var outPutCmd bool

var rootCmd = &cobra.Command{
	Use:   "client_project",
	Short: "Client for solving problems",
	Long: `Client for solving problems like FizzBuzz, FibonacciVerifier, PrimeClassifier.
Example usage: go run main.go --problem=FizzBuzz --min=20 --max=100 --count=50 --output_file or --output_cmd `,
	RunE: func(cmd *cobra.Command, args []string) error {
		data := Data{
			Problem:      problem,
			CountNumbers: countNumbers,
			MinNumber:    minNumber,
			MaxNumber:    maxNumber,
			OutPutFile:   outPutFile,
			OutPutCmd:    outPutCmd,
			Kill:         false,
		}
		if !outPutFile && !outPutCmd {
			outPutCmd = true
		}

		jsonData, err := json.Marshal(data)
		if err != nil {
			log.Fatalf("Error marshalling data: %v", err)
		}

		fmt.Println("Connecting...")
		conn, err := util.ConnectToServer("localhost:65535")
		if err != nil {
			return fmt.Errorf("error connecting to problemsolver: %v", err)
		}
		fmt.Println("Connected")
		defer conn.Close()

		err = util.SendData(jsonData, conn)
		if err != nil {
			return fmt.Errorf("error sending data: %v", err)
		}

		reader, err := util.ReceiveData("localhost:62000")
		if err != nil {
			return fmt.Errorf("error receiving data: %v", err)
		}

		buffer := make([]byte, 4096)
		var result Result
		var jsonDataBytes bytes.Buffer

		for {

			n, err := reader.Read(buffer)
			if err != nil {
				if err == io.EOF {
					break
				}
				fmt.Println("Error reading from socket:", err)

			}

			jsonDataBytes.Write(buffer[:n])
		}

		err = json.Unmarshal(jsonDataBytes.Bytes(), &result)
		if err != nil {
			fmt.Println(("error"))
		}

		if outPutFile {
			util.WriteResultToFile(result.Numbers, result.Results, problem)
		}

		if outPutCmd {
			for i, number := range result.Numbers {
				fmt.Printf("%d %s\n", number, result.Results[i])
			}
		}

		return nil
	},
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		os.Exit(1)
	}
}

func init() {
	rootCmd.Flags().StringVarP(&problem, "problem", "p", "FizzBuzz", "Problem to be resolved")
	rootCmd.Flags().Int64VarP(&minNumber, "min", "m", 0, "Minimum number")
	rootCmd.Flags().Int64VarP(&maxNumber, "max", "M", 100, "Maximum number")
	rootCmd.Flags().Int64VarP(&countNumbers, "count", "c", 10, "Count of numbers")
	rootCmd.Flags().BoolVarP(&outPutFile, "output_file", "o", false, "Output file")
	rootCmd.Flags().BoolVarP(&outPutCmd, "output_cmd", "t", false, "Output cmd")
}
