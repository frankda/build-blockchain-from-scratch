package base

import "fmt"

type FieldElementStruct struct {
	Num   int
	Prime int
}

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
