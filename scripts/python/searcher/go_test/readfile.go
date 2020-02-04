package main

import "C"

import (
	"bufio"
	"bytes"
	"encoding/csv"
	"fmt"
	"io"
	"io/ioutil"
	"regexp"
	"strings"
	"sync"

	"github.com/jszwec/csvutil"
)

var mtx sync.Mutex
var reSpace = regexp.MustCompile(`\s{2,}|\t`)

type reader struct {
	sc  *bufio.Scanner
	buf bytes.Buffer
}

func newReader(r io.Reader) *reader {
	return &reader{
		sc: bufio.NewScanner(r),
	}
}

func (r *reader) Read(p []byte) (int, error) {
	for r.sc.Scan() {
		line := r.sc.Text()
		if line == "" || strings.HasPrefix(line, "//") || strings.HasPrefix(line, "HCONTEXT") {
			continue
		}

		line = reSpace.ReplaceAllString(line, ",")
		line = strings.ReplaceAll(line, `" "`, `","`)
		r.buf.WriteString(line)
		r.buf.WriteByte('\n')
		break
	}

	if err := r.sc.Err(); err != nil {
		return 0, err
	}
	return r.buf.Read(p)
}

type GPlay struct {
	Command     string
	Desc1       string
	Desc2       string
	Combination string
}

var GplayHeader []string

func init() {
	h, err := csvutil.Header(GPlay{}, "")
	if err != nil {
		panic(err)
	}
	GplayHeader = h
}

//export ReadKeyFile
func ReadKeyFile(msg string) int {
	var b strings.Builder

	data, err := ioutil.ReadFile("gplay")

	if _, err := io.Copy(&b, newReader(strings.NewReader(string(data)))); err != nil {
		panic(err)
	}
	mtx.Lock()
	defer mtx.Unlock()

	fmt.Println(msg)
	fmt.Println("Normalized file:")
	fmt.Println(b.String())

	csvr := csv.NewReader(strings.NewReader(b.String()))
	dec, err := csvutil.NewDecoder(csvr, GplayHeader...)
	if err != nil {
		panic(err)
	}

	var gplays []GPlay
	if err := dec.Decode(&gplays); err != nil {
		panic(err)
	}

	for _, gplay := range gplays {
		fmt.Printf("%+v\n", gplay)
	}
	return 1
}

//export ReadKeyFilePtr
func ReadKeyFilePtr(msg *string) int {
	return ReadKeyFile(*msg)
}

func main() {}
