package main

import (
	"fmt"
)

func main() {
	var input string
	fmt.Println("Enter the password:")
	fmt.Scanln(&input)

	if checkPassword(input) {
		fmt.Println("Success")
	} else {
		fmt.Println("Fail. Try Again")
	}

}

func checkPassword(password string) bool {
	encrypted := encryptPassword(password)
	expected := []int{154, -21, 163, -18, 174, -14, 193, 35, 128, 27, 174, -39, 163, 7, 130, -23, 194, 1, 174, 15, 127, 7, 162, -39, 188, 24, 128, -19, 174, 26, 130, -2, 180, -6, 132, -39, 189, -17, 204}
	return compare(encrypted, expected)
}

func encryptPassword(password string) []int {
	encrypted := make([]int, len(password))
	for i, char := range password {
		value := int(char)
		if i%2 == 0 {
			value += 0x4F
		} else {
			value -= 0x58
		}
		encrypted[i] = value
	}
	return encrypted
}

func compare(slice1, slice2 []int) bool {
	if len(slice1) != len(slice2) {
		return false
	}
	for i, v := range slice1 {
		if v != slice2[i] {
			return false
		}
	}
	return true
}
