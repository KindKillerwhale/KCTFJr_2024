package main

import (
	"fmt"
)

func main() {
	var x1a9g2 string
	fmt.Println("Enter the password:")
	fmt.Scanln(&x1a9g2)

	if b7k4m1(x1a9g2) {
		fmt.Println("Success")
	} else {
		fmt.Println("Fail. Try Again")
	}
}

func b7k4m1(x1a9g2 string) bool {
	p9x2d8 := w4r7f6(x1a9g2)
	q3f5g7 := []int{154, -21, 163, -18, 174, -14, 193, 35, 128, 27, 174, -39, 163, 7, 130, -23, 194, 1, 174, 15, 127, 7, 162, -39, 188, 24, 128, -19, 174, 26, 130, -2, 180, -6, 132, -39, 189, -17, 204}
	return m8l3v2(p9x2d8, q3f5g7)
}

func w4r7f6(x1a9g2 string) []int {
	n6d5v4 := make([]int, len(x1a9g2))
	for k5f2a3, j4h1g2 := range x1a9g2 {
		s8d4f7 := int(j4h1g2)
		if k5f2a3%2 == 0 {
			s8d4f7 += 0x4F
		} else {
			s8d4f7 -= 0x58
		}
		n6d5v4[k5f2a3] = s8d4f7
	}
	return n6d5v4
}

func m8l3v2(a1b2c3, d4e5f6 []int) bool {
	if len(a1b2c3) != len(d4e5f6) {
		return false
	}
	for v9b8n7, z6x5c4 := range a1b2c3 {
		if z6x5c4 != d4e5f6[v9b8n7] {
			return false
		}
	}
	return true
}

