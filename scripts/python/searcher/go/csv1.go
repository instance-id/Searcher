package main

import (
	"bufio"
	"bytes"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"time"
)

var writeFile = []string{"new", "new2"}

type Hcontext struct {
	HContext    string
	Context     string
	Description string
	Title       string `json:"title,omitempty"`
}

type Hotkeys struct {
	HotkeySymbol string
	Label        string
	Description  string
	Assignments  string
}

var reSpace = regexp.MustCompile(`\s{2,}|\t`)
var space = regexp.MustCompile(`\s+`)

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

		inlineComment := "// "
		line = strings.Split(line, inlineComment)[0]

		if line == "" || strings.HasPrefix(line, "    ") || strings.HasPrefix(line, "//") || strings.HasPrefix(line, "HCONTEXT") || strings.HasPrefix(line, "#include") {
			continue
		}

		line = space.ReplaceAllString(line, " ")
		line = strings.ReplaceAll(line, `" "`, `","`)
		line = strings.ReplaceAll(line, `" `, `",`)
		line = strings.ReplaceAll(line, ` "`, `,"`)
		line = strings.ReplaceAll(line, `, "`, `,"`)
		line = strings.ReplaceAll(line, `, `, ` `)
		line = strings.ReplaceAll(line, `\",`, ``)

		r.buf.WriteString(line)
		r.buf.WriteString(",,")
		r.buf.WriteByte('\n')
		break
	}

	if err := r.sc.Err(); err != nil {
		return 0, err
	}
	return r.buf.Read(p)
}

func WriteFile(data []string) {
	t := time.Now()
	f, err := os.Create(fmt.Sprintf("E:\\GitHub\\Searcher\\scripts\\python\\searcher\\go\\output\\%stest.txt", t.Format("20060102150405.000000")))
	if err != nil {
		fmt.Println(err)
		return
	}

	datawriter := bufio.NewWriter(f)

	for _, data1 := range data {
		_, _ = datawriter.WriteString(data1 + "\n")
	}
	datawriter.Flush()
	f.Close()
}

func getEnv(key, fallback string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value + "/houdini/config/Hotkeys"
	}
	return fallback
}

func main() {
	var files []string

	root := getEnv("HFS", "houdini/config/Hotkeys/")
	err := filepath.Walk(root, func(path string, info os.FileInfo, err error) error {
		files = append(files, path)
		return nil
	})
	if err != nil {
		fmt.Println(fmt.Sprintf("Error Opening File: %s", err))
	}

	for _, file := range files {
		if file == "houdini/config/Hotkeys/" {
			continue
		}

		fmt.Println(fmt.Sprintf("File Name : %s --------------------------", file))
		csvFile, err := ioutil.ReadFile(file)
		if err != nil {
			fmt.Println(fmt.Sprintf("Error Opening File: %s", err))
		}

		var b strings.Builder
		if _, err := io.Copy(&b, newReader(strings.NewReader(string(csvFile)))); err != nil {
			fmt.Println(fmt.Sprintf("Error With Reader: %s", err))
		}
		fmt.Println(b.String())
		reader := csv.NewReader(strings.NewReader(b.String()))

		var hotkeys []Hotkeys
		var counter = 0
		for {
			line, err := reader.Read()
			if err == io.EOF {
				break
			}

			hotkeys = append(hotkeys, Hotkeys{
				HotkeySymbol: line[0],
				Label:        line[1],
				Description:  line[2],
				Assignments:  line[3],
			})
			fmt.Printf("Current Counter: %d ", counter)
			counter++
		}

		hcontextJson, err := json.Marshal(hotkeys)
		if err != nil {
			fmt.Println(fmt.Sprintf("Error Marshalling Data: %s", err))
		}

		fmt.Println(string(hcontextJson))
	}
}
