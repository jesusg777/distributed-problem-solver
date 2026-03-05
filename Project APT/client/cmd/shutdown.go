package cmd

import (
	"cliente_project/util"
	"encoding/json"
	"fmt"
	"log"
	"strings"

	"github.com/spf13/cobra"
)

var inputPassword string

var shutdownCmd = &cobra.Command{
	Use:   "shutdown",
	Short: "Shutdown the server",
	Long:  `Shutdown the server by providing the correct password`,
	RunE: func(cmd *cobra.Command, args []string) error {
		fmt.Println("Starting shutdown...")

		if inputPassword == "" {
			return fmt.Errorf("a password is required, use -p 'password'")
		}

		actualPasswords := util.Read()
		if len(actualPasswords) == 0 {
			return fmt.Errorf("the system doesn't have a set password")
		}

		hashes := strings.Split(actualPasswords, ",")
		if util.CheckPasswordHash(inputPassword, hashes) {
			fmt.Println("Password is correct.")
		} else {
			fmt.Println("Password is incorrect.")
		}

		if !util.CheckPasswordHash(inputPassword, hashes) {
			return fmt.Errorf("the provided password is incorrect")
		}

		data := Data{
			Kill: true,
		}

		jsonData, err := json.Marshal(data)
		if err != nil {
			log.Fatalf("error: %v", err)
		}

		conn, err := util.ConnectToServer("localhost:65535")
		if err != nil {
			return fmt.Errorf("error connecting to server: %v", err)
		}
		defer conn.Close()

		err = util.SendData(jsonData, conn)
		if err != nil {
			return fmt.Errorf("error sending data: %v", err)
		}

		return nil
	},
}

func init() {
	rootCmd.AddCommand(shutdownCmd)
	shutdownCmd.Flags().StringVarP(&inputPassword, "password", "p", "", "the password to authorize shutdown")
}
