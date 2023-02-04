package base

import (
	"fmt"
	"reflect"
	"testing"
)

func TestFieldElement(t *testing.T) {
	testCases := []struct {
		num      int
		prime    int
		expected *FieldElementStruct
		err      error
	}{
		{2, 5, &FieldElementStruct{2, 5}, nil},
		{6, 5, nil, fmt.Errorf("num 6 not in field range 0 to 4")},
		{-1, 5, nil, fmt.Errorf("num -1 not in field range 0 to 4")},
	}

	for _, tt := range testCases {
		result, err := FieldElement(tt.num, tt.prime)
		if !reflect.DeepEqual(result, tt.expected) || (err != nil && err.Error() != tt.err.Error()) {
			t.Errorf("FieldElement(%d, %d) = %v, %v, expected %v, %v", tt.num, tt.prime, result, err, tt.expected, tt.err)
		}
	}
}

func TestEquals(t *testing.T) {
	testCases := []struct {
		a, b FieldElementStruct
		want bool
	}{
		{FieldElementStruct{2, 3}, FieldElementStruct{2, 3}, true},
		{FieldElementStruct{2, 3}, FieldElementStruct{3, 3}, false},
		{FieldElementStruct{2, 3}, FieldElementStruct{2, 4}, false},
	}
	for _, tt := range testCases {
		got := tt.a.Equals(&tt.b)
		if got != tt.want {
			t.Errorf("%v.Equals(%v) == %t, want %t", tt.a, tt.b, got, tt.want)
		}
	}
}

func TestNotEquals(t *testing.T) {
	testCases := []struct {
		a, b FieldElementStruct
		want bool
	}{
		{FieldElementStruct{2, 3}, FieldElementStruct{2, 3}, false},
		{FieldElementStruct{2, 3}, FieldElementStruct{3, 3}, true},
		{FieldElementStruct{2, 3}, FieldElementStruct{2, 4}, true},
	}
	for _, tt := range testCases {
		got := tt.a.NotEquals(&tt.b)
		if got != tt.want {
			t.Errorf("%v.NotEquals(%v) == %t, want %t", tt.a, tt.b, got, tt.want)
		}
	}
}

func TestAdd(t *testing.T) {
	// Test cases
	testCases := []struct {
		f      *FieldElementStruct
		other  *FieldElementStruct
		result *FieldElementStruct
		err    error
	}{
		{
			f:      &FieldElementStruct{Num: 6, Prime: 5},
			other:  &FieldElementStruct{Num: 2, Prime: 5},
			result: &FieldElementStruct{Num: 3, Prime: 5},
			err:    nil,
		},
		{
			f:      &FieldElementStruct{Num: 4, Prime: 7},
			other:  &FieldElementStruct{Num: 3, Prime: 5},
			result: nil,
			err:    fmt.Errorf("cannot add two numbers in different Fields"),
		},
		{
			f:      &FieldElementStruct{Num: 10, Prime: 17},
			other:  &FieldElementStruct{Num: 7, Prime: 17},
			result: &FieldElementStruct{Num: 0, Prime: 17},
			err:    nil,
		},
		{
			f:      &FieldElementStruct{Num: -5, Prime: 17},
			other:  &FieldElementStruct{Num: -7, Prime: 17},
			result: &FieldElementStruct{Num: 5, Prime: 17},
			err:    nil,
		},
	}

	// Iterate over test cases and compare expected results with actual results
	for _, tt := range testCases {
		result, err := tt.f.Add(tt.other)
		if tt.err != nil && err == nil {
			t.Errorf("Unexpected error: got %v, want %v", err, tt.err)
		}
		if result == nil && tt.result != nil || result != nil && tt.result == nil {
			t.Errorf("Unexpected result: got %v, want %v", result, tt.result)
		} else if result != nil && tt.result != nil && (*result != *tt.result) {
			t.Errorf("Unexpected result: got %v, want %v", result, tt.result)
		}
	}
}

func TestSub(t *testing.T) {
	// Test cases
	testCases := []struct {
		f      *FieldElementStruct
		other  *FieldElementStruct
		result *FieldElementStruct
		err    error
	}{
		{
			f:      &FieldElementStruct{Num: 29, Prime: 31},
			other:  &FieldElementStruct{Num: 4, Prime: 31},
			result: &FieldElementStruct{Num: 25, Prime: 31},
			err:    nil,
		},
		{
			f:      &FieldElementStruct{Num: 15, Prime: 31},
			other:  &FieldElementStruct{Num: 30, Prime: 31},
			result: &FieldElementStruct{Num: 16, Prime: 31},
			err:    nil,
		},
	}

	// Iterate over test cases and compare expected results with actual results
	for _, tt := range testCases {
		result, err := tt.f.Sub(tt.other)
		if tt.err != nil && err == nil {
			t.Errorf("Unexpected error: got %v, want %v", err, tt.err)
		}
		if result == nil && tt.result != nil || result != nil && tt.result == nil {
			t.Errorf("Unexpected result: got %v, want %v", result, tt.result)
		} else if result != nil && tt.result != nil && (*result != *tt.result) {
			t.Errorf("Unexpected result: got %v, want %v", result, tt.result)
		}
	}
}

func TestMul(t *testing.T) {
	// Test cases
	testCases := []struct {
		f      *FieldElementStruct
		other  *FieldElementStruct
		result *FieldElementStruct
		err    error
	}{
		{
			f:      &FieldElementStruct{Num: 24, Prime: 31},
			other:  &FieldElementStruct{Num: 19, Prime: 31},
			result: &FieldElementStruct{Num: 22, Prime: 31},
			err:    nil,
		},
	}

	// Iterate over test cases and compare expected results with actual results
	for _, tt := range testCases {
		result, err := tt.f.Mul(tt.other)
		if tt.err != nil && err == nil {
			t.Errorf("Unexpected error: got %v, want %v", err, tt.err)
		}
		if result == nil && tt.result != nil || result != nil && tt.result == nil {
			t.Errorf("Unexpected result: got %v, want %v", result, tt.result)
		} else if result != nil && tt.result != nil && (*result != *tt.result) {
			t.Errorf("Unexpected result: got %v, want %v", result, tt.result)
		}
	}
}

func TestPow(t *testing.T) {
	// Test cases
	testCases := []struct {
		f      *FieldElementStruct
		other  int
		result *FieldElementStruct
		err    error
	}{
		{
			f:      &FieldElementStruct{Num: 17, Prime: 31},
			other:  3,
			result: &FieldElementStruct{Num: 15, Prime: 31},
			err:    nil,
		},
	}

	// Iterate over test cases and compare expected results with actual results
	for _, tt := range testCases {
		result, err := tt.f.Pow(tt.other)
		if tt.err != nil && err == nil {
			t.Errorf("Unexpected error: got %v, want %v", err, tt.err)
		}
		if result == nil && tt.result != nil || result != nil && tt.result == nil {
			t.Errorf("Unexpected result: got %v, want %v", result, tt.result)
		} else if result != nil && tt.result != nil && (*result != *tt.result) {
			t.Errorf("Unexpected result: got %v, want %v", result, tt.result)
		}
	}
}

func TestDiv(t *testing.T) {
	// Test cases
	testCases := []struct {
		f      *FieldElementStruct
		other  *FieldElementStruct
		result *FieldElementStruct
		err    error
	}{
		{
			f:      &FieldElementStruct{Num: 3, Prime: 31},
			other:  &FieldElementStruct{Num: 24, Prime: 31},
			result: &FieldElementStruct{Num: 4, Prime: 31},
			err:    nil,
		},
	}

	// Iterate over test cases and compare expected results with actual results
	for _, tt := range testCases {
		result, err := tt.f.Mul(tt.other)
		if tt.err != nil && err == nil {
			t.Errorf("Unexpected error: got %v, want %v", err, tt.err)
		}
		if result == nil && tt.result != nil || result != nil && tt.result == nil {
			t.Errorf("Unexpected result: got %v, want %v", result, tt.result)
		} else if result != nil && tt.result != nil && (*result != *tt.result) {
			t.Errorf("Unexpected result: got %v, want %v", result, tt.result)
		}
	}
}