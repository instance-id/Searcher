package main

import (
	"fmt"
	"io/ioutil"
	"regexp"
	"strings"
)

func main() {
	customHotkeyData, err := ioutil.ReadFile("file.txt")
	if err != nil {
		fmt.Println(fmt.Sprintf("Error Opening File: %s", err))
	}

	customStr := []string{string(customHotkeyData)}
	val := GetStringFromQuotes(customStr)
	val2 := GetStringFromQuotes(customStr)
	val3 := StrExtract(string(customHotkeyData))
	fmt.Println(val[2])
	fmt.Println(val2[2])
	fmt.Println(val3[0])
	//fmt.Print(string(customHotkeyData))
}

func StrExtract(word string) []string {
	r, _ := regexp.Compile(`"(.*?)"`)
	result := r.FindAllString(word, -1)
	return result
}

func GetStringFromQuotes(parts []string) []string {
	str := strings.Join(parts, " ")
	inQuote := false
	f := func(c rune) bool {
		switch {
		case c == '"':
			inQuote = !inQuote
			return false
		case inQuote:
			return false
		default:
			return c == ' '
		}
	}
	return strings.FieldsFunc(str, f)
}

func GetStringFromQuotes2(parts []string) []string {
	re := regexp.MustCompile(`"[^"]+"|\S+`)
	str := strings.Join(parts, " ")
	return re.FindAllString(str, -1)
}
