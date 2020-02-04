package main

//
//import (
//	"bufio"
//	"bytes"
//	"encoding/csv"
//	"fmt"
//	"io"
//	"regexp"
//	"strings"
//
//	"github.com/jszwec/csvutil"
//)
//
//var data = `//
//// Gplay hotkeys
////
//
//HCONTEXT gplay "GPLAY Geometry Viewer" "These keys apply to the Geometry Viewer application."
//
//// File menu
//gplay.open		"Open"			"Open"			Alt+O Ctrl+O
//gplay.quit		"Quit"			"Quit"			Alt+Q Ctrl+Q
//
//// Display menu
//gplay.display_info	"Geometry Info"		"Geometry Info"		Alt+I
//gplay.unpack		"Unpack Geometry"	"Unpack Geometry"	Alt+U
//gplay.display_ssheet	"Geometry Spreadsheet"	"Geometry Speadsheet"	Alt+S
//gplay.flipbook		"Flipbook Current Viewport" "Flipbook the currently selected viewport"	Alt+F
//gplay.display_prefs	"Preferences"		"Preferences"
//
//// Help menu
//gplay.help_menu		"Help Menu"		"Help Menu"		Alt+H
//
//// Commands not in menus
//gplay.quick_quit	"Quick Quit"		"Quick Quit"		Q
//gplay.next_geo		"Next Geometry"		"Next Geometry"		N
//gplay.prev_geo		"Previous Geometry"	"Previous Geometry"	P
//gplay.stop_play		"Stop Play"		"Stop Play"		Space
//`
//
//var reSpace = regexp.MustCompile(`\s{2,}|\t`)
//
//type reader struct {
//	sc  *bufio.Scanner
//	buf bytes.Buffer
//}
//
//func newReader(r io.Reader) *reader {
//	return &reader{
//		sc: bufio.NewScanner(r),
//	}
//}
//
//func (r *reader) Read(p []byte) (int, error) {
//	for r.sc.Scan() {
//		line := r.sc.Text()
//		if line == "" || strings.HasPrefix(line, "//") || strings.HasPrefix(line, "HCONTEXT") {
//			continue
//		}
//
//		line = reSpace.ReplaceAllString(line, ",")
//		line = strings.ReplaceAll(line, `" "`, `","`)
//		r.buf.WriteString(line)
//		r.buf.WriteByte('\n')
//		break
//	}
//
//	if err := r.sc.Err(); err != nil {
//		return 0, err
//	}
//	return r.buf.Read(p)
//}
//
//type GPlay struct {
//	Command     string
//	Desc1       string
//	Desc2       string
//	Combination string
//}
//
//var GplayHeader []string
//
//func init() {
//	h, err := csvutil.Header(GPlay{}, "")
//	if err != nil {
//		panic(err)
//	}
//	GplayHeader = h
//}
//
//func main() {
//	var b strings.Builder
//	if _, err := io.Copy(&b, newReader(strings.NewReader(data))); err != nil {
//		panic(err)
//	}
//	fmt.Println("Normalized file:")
//	fmt.Println(b.String())
//
//	csvr := csv.NewReader(strings.NewReader(b.String()))
//	dec, err := csvutil.NewDecoder(csvr, GplayHeader...)
//	if err != nil {
//		panic(err)
//	}
//
//	var gplays []GPlay
//	if err := dec.Decode(&gplays); err != nil {
//		panic(err)
//	}
//
//	fmt.Println("Decoded slice of structs")
//	for _, gplay := range gplays {
//		fmt.Printf("%+v\n", gplay)
//	}
//}
