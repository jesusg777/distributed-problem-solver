package util

import (
	"crypto/sha256"
	"encoding/hex"
)

func HashPassword(password string) string {
	hasher := sha256.New()
	hasher.Write([]byte(password))
	return hex.EncodeToString(hasher.Sum(nil))
}

func CheckPasswordHash(password string, hashes []string) bool {
	hashedPassword := HashPassword(password)
	for _, hash := range hashes {
		if hash == hashedPassword {
			return true
		}
	}
	return false
}
