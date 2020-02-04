package models

import (
	"time"

	. "github.com/instance-id/Searcher/utils"

	"github.com/sarulabs/di/v2"
)

type QueryStatementDataAccessObject struct{}

type QueryStatement struct {
	Id           int64     `xorm:"'id' pk autoincr notnull"`
	HotkeySymbol string    `xorm:"'hotkey_symbol' not null VARCHAR(75)"`
	Context      string    `xorm:"'context' VARCHAR(75)"`
	Label        string    `xorm:"'label' index(par_ind) VARCHAR(75)"`
	Description  string    `xorm:"'description' VARCHAR(75)"`
	Assignments  string    `xorm:"'assignments' VARCHAR(75)"`
	LastModified time.Time `xorm:"'lastmodified' created"`
}

var QueryStatementDAO *QueryStatementDataAccessObject

func (q *QueryStatementDataAccessObject) TableName() string {
	return "hotkeys"
}

// --- Add new user to database -------------------------------------------------------------------
func (q *QueryStatementDataAccessObject) Query(di di.Container, input string) []map[string][]byte {
	db := DatabaseAccessContainer(di)
	//log := LogAccessContainer(di)

	sql := ("SELECT id, label, assignments,context, description FROM hotkeys WHERE label LIKE '%" + input + "%'")
	result, err := db.Query(sql)
	LogFatalf("Unable to insert hotkey", err)
	//log.Infof("Data from query : %s", result[0])
	return result
}
