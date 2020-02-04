package models

import (
	"bufio"
	"bytes"
	"encoding/csv"
	"fmt"
	"io"
	"io/ioutil"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"time"

	. "github.com/instance-id/Searcher/utils"
	"github.com/sarulabs/di/v2"
	"xorm.io/xorm"
)

type HotkeysDataAccessObject struct{}

type Hotkeys struct {
	Id           int64     `xorm:"'id' pk autoincr notnull"`
	HotkeySymbol string    `xorm:"'hotkey_symbol' not null VARCHAR(75)"`
	Context      string    `xorm:"'context' VARCHAR(75)"`
	Label        string    `xorm:"'label' index(par_ind) VARCHAR(75)"`
	Description  string    `xorm:"'description' VARCHAR(75)"`
	Assignments  string    `xorm:"'assignments' VARCHAR(75)"`
	LastModified time.Time `xorm:"'lastmodified' created"`
}

var HotkeysDAO *HotkeysDataAccessObject

func (hk *HotkeysDataAccessObject) TableName() string {
	return "hotkeys"
}

// --- Create new hotkeys object --------------------------------------------------------------------
func NewHotkeysObject(hotkeySymbol string, context string, label string, description string, assignments string) *Hotkeys {
	return &Hotkeys{
		HotkeySymbol: hotkeySymbol,
		Context:      context,
		Label:        label,
		Description:  description,
		Assignments:  assignments,
	}
}

// --- Add new user to database -------------------------------------------------------------------
func (hk *HotkeysDataAccessObject) Query(hotkeys *Hotkeys, di di.Container) {
	db := DatabaseAccessContainer(di)
	_, err := db.Table(HotkeysDAO.TableName()).InsertOne(hotkeys)
	LogFatalf("Unable to insert hotkey", err)
	log := LogAccessContainer(di)
	log.Infof("Data from insert: %v", hotkeys.Id)
}

// --- Add new user to database -------------------------------------------------------------------
func (hk *HotkeysDataAccessObject) AddHotkeys(hotkeys *Hotkeys, di di.Container) {
	db := DatabaseAccessContainer(di)
	_, err := db.Table(HotkeysDAO.TableName()).InsertOne(hotkeys)
	LogFatalf("Unable to insert hotkey", err)
	log := LogAccessContainer(di)
	log.Infof("Data from insert: %v", hotkeys.Id)
}

// --- Add new user to database -------------------------------------------------------------------
func (hk *HotkeysDataAccessObject) AddAllHotkeys(di di.Container) {
	db := DatabaseAccessContainer(di)
	UpdateAll(db)
}

// --- Add all hotkeys ----------------------------------------------------------------------------
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

func UpdateAll(db *xorm.Engine) {
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

		for {
			line, err := reader.Read()
			if err == io.EOF {
				break
			}
			hkey := NewHotkeysObject(line[0], filepath.Base(file), line[1], line[2], line[3])
			_, err = db.Table(HotkeysDAO.TableName()).InsertOne(hkey)
		}
	}
}
