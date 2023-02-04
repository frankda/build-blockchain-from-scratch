package base

import (
	"fmt"
	"math"
)

type FieldElementStruct struct {
	Num   int
	Prime int
}

// utils
func extendedEuclideanAlgorithm(a, b int) (int, int, int) {
	if b == 0 {
		return 1, 0, a
	}
	x, y, gcd := extendedEuclideanAlgorithm(b, a%b)
	return y, x - (a/b)*y, gcd
}

func Inverse(a int, p int) int {
	x, _, gcd := extendedEuclideanAlgorithm(int(a), p)
	if gcd != 1 {
		// a has no modular inverse
		return 0
	}
	return (x%p + p) % p
}

// finite field methods
func FieldElement(num int, prime int) (*FieldElementStruct, error) {
	if num > prime || num < 0 {
		return nil, fmt.Errorf("num %d not in field range 0 to %d", num, prime-1)
	}
	return &FieldElementStruct{Num: num, Prime: prime}, nil
}

func (f *FieldElementStruct) Equals(other *FieldElementStruct) bool {
	return f.Num == other.Num && f.Prime == other.Prime
}

func (f *FieldElementStruct) NotEquals(other *FieldElementStruct) bool {
	return f.Num != other.Num || f.Prime != other.Prime
}

func (f *FieldElementStruct) Add(other *FieldElementStruct) (*FieldElementStruct, error) {
	if f.Prime != other.Prime {
		return nil, fmt.Errorf("cannot add two numbers in different Fields")
	}
	sum := f.Num + other.Num
	for sum < 0 {
		sum += f.Prime
	}
	return &FieldElementStruct{Num: sum % f.Prime, Prime: f.Prime}, nil
}

func (f *FieldElementStruct) Sub(other *FieldElementStruct) (*FieldElementStruct, error) {
	if f.Prime != other.Prime {
		return nil, fmt.Errorf("cannot sub two numbers in different Fields")
	}
	sum := f.Num - other.Num
	for sum < 0 {
		sum += f.Prime
	}
	return &FieldElementStruct{Num: sum % f.Prime, Prime: f.Prime}, nil
}

func (f *FieldElementStruct) Mul(other *FieldElementStruct) (*FieldElementStruct, error) {
	if f.Prime != other.Prime {
		return nil, fmt.Errorf("cannot multiple two numbers in different Fields")
	}
	sum := f.Num * other.Num
	for sum < 0 {
		sum += f.Prime
	}
	return &FieldElementStruct{Num: sum % f.Prime, Prime: f.Prime}, nil
}

func (f *FieldElementStruct) Pow(index int) (*FieldElementStruct, error) {
	result := int(math.Pow(float64(f.Num), float64(index)))
	for result < 0 {
		result += f.Prime
	}
	return &FieldElementStruct{Num: result % f.Prime, Prime: f.Prime}, nil
}

func (f *FieldElementStruct) Truediv(other *FieldElementStruct) (*FieldElementStruct, error) {
	if f.Prime != other.Prime {
		return nil, fmt.Errorf("cannot multiple two numbers in different Fields")
	}
	index := f.Prime - 2
	result := f.Num * int(math.Pow(float64(other.Num), float64(index)))
	return &FieldElementStruct{Num: result, Prime: f.Prime}, nil
}
