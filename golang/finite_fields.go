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

func (f FieldElementStruct) Equals(other *FieldElementStruct) bool {
	return f.Num == other.Num && f.Prime == other.Prime
}
