package base

import (
	"fmt"
	"reflect"
	"testing"
)

func TestFieldElement(t *testing.T) {
	tests := []struct {
		num      int
		prime    int
		expected *FieldElementStruct
		err      error
	}{
		{2, 5, &FieldElementStruct{2, 5}, nil},
		{6, 5, nil, fmt.Errorf("num 6 not in field range 0 to 4")},
		{-1, 5, nil, fmt.Errorf("num -1 not in field range 0 to 4")},
	}

	for _, test := range tests {
		result, err := FieldElement(test.num, test.prime)
		if !reflect.DeepEqual(result, test.expected) || (err != nil && err.Error() != test.err.Error()) {
			t.Errorf("FieldElement(%d, %d) = %v, %v, expected %v, %v", test.num, test.prime, result, err, test.expected, test.err)
		}
	}
}

func TestEquals(t *testing.T) {
	fieldElement1, _ := FieldElement(2, 5)
	fieldElement2, _ := FieldElement(2, 5)
	if fieldElement1.Equals(fieldElement2) == false {
		t.Errorf("Expected FieldElement(2, 5) equals FieldElement(2, 5)")
	}
}
