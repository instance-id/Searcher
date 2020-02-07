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
var whichReader = 0

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

// --- Add new hotkeys to database -------------------------------------------------------------------
func (hk *HotkeysDataAccessObject) AddHotkeys(hotkeys *Hotkeys, di di.Container) {
	db := DatabaseAccessContainer(di)
	_, err := db.Table(HotkeysDAO.TableName()).InsertOne(hotkeys)
	LogFatalf("Unable to insert hotkey", err)
	log := LogAccessContainer(di)
	log.Infof("Data from insert: %v", hotkeys.Id)
}

// --- Add all hotkeys to database -------------------------------------------------------------------
func (hk *HotkeysDataAccessObject) ProcessHotkeys(di di.Container, method string) {
	db := DatabaseAccessContainer(di)
	ParseHotkeys(db, method)
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

		if whichReader == 0 {
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

		} else if whichReader == 1 {
			if line == "" || !strings.HasPrefix(line, "HCONTEXT") || strings.HasPrefix(line, "    ") || strings.HasPrefix(line, "//") || strings.HasPrefix(line, "#include") {
				continue
			}

			line = space.ReplaceAllString(line, " ")
			line = strings.ReplaceAll(line, `" "`, `","`)
			line = strings.ReplaceAll(line, `" `, `",`)
			line = strings.ReplaceAll(line, ` "`, `,"`)
			line = strings.ReplaceAll(line, `, "`, `,"`)
			line = strings.ReplaceAll(line, `, `, ` `)
			line = strings.ReplaceAll(line, `\",`, ``)
			line = strings.ReplaceAll(line, `HCONTEXT`, ``)

			r.buf.WriteString(line)
			r.buf.WriteString(",,")
			r.buf.WriteByte('\n')
			break
		}
	}

	if err := r.sc.Err(); err != nil {
		return 0, err
	}
	return r.buf.Read(p)
}

func getEnv(key, fallback string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value + "/houdini/config/Hotkeys"
	}
	return fallback
}

func ParseHotkeys(db *xorm.Engine, method string) {
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

		whichReader = 0
		var hk strings.Builder
		if _, err := io.Copy(&hk, newReader(strings.NewReader(string(csvFile)))); err != nil {
			fmt.Println(fmt.Sprintf("Error With Reader: %s", err))
		}
		//fmt.Println(hk.String())

		whichReader = 0
		reader := csv.NewReader(strings.NewReader(hk.String()))
		for {
			line, err := reader.Read()
			if err == io.EOF {
				break
			}

			method = "insert"

			hkey := NewHotkeysObject(line[0], filepath.Base(file), line[1], line[2], line[3])
			if method == "insert" {
				_, err := db.Table(HotkeysDAO.TableName()).Insert(hkey)
				if err != nil {
					fmt.Println(fmt.Sprintf("Error inserting record: %s", err))
				}

			} else if method == "update" {
				_, err := db.Table(HotkeysDAO.TableName()).Update(hkey)
				if err != nil {
					fmt.Println(fmt.Sprintf("Error updating record: %s", err))
				}
			}
		}

		whichReader = 1
		var hc strings.Builder
		if _, err := io.Copy(&hc, newReader(strings.NewReader(string(csvFile)))); err != nil {
			fmt.Println(fmt.Sprintf("Error With Reader: %s", err))
		}

		whichReader = 1
		hcreader := csv.NewReader(strings.NewReader(hc.String()))

		for {
			hcline, err := hcreader.Read()
			if err == io.EOF {
				break
			}

			hcontext := NewHContextObject(hcline[0], hcline[0], hcline[2], hcline[1])
			if method == "insert" {
				_, err = db.Table(HContextDAO.TableName()).Insert(hcontext)
				if err != nil {
					fmt.Println(fmt.Sprintf("Error updating record: %s", err))
				}

			} else if method == "update" {
				_, err := db.Table(HContextDAO.TableName()).Update(hcontext)
				if err != nil {
					fmt.Println(fmt.Sprintf("Error updating record: %s", err))
				}
			}

		}
	}
}
