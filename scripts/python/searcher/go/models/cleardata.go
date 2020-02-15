package models

import (
	"github.com/sirupsen/logrus"

	. "github.com/instance-id/Searcher/utils"

	"github.com/sarulabs/di/v2"
)

type ClearDataDataAccessObject struct{}

var ClearDataDAO *ClearDataDataAccessObject

func (q *ClearDataDataAccessObject) TableName() string {
	return "hotkeys"
}

// --- Add new user to database -------------------------------------------------------------------
func (q *ClearDataDataAccessObject) ClearData(di di.Container) {
	db := DatabaseAccessContainer(di)

	sql := "DELETE FROM hotkeys"
	sql2 := "DELETE FROM sqlite_sequence WHERE name='hotkeys'"
	result, err := db.Query(sql)
	LogFatalf("Unable to clear DB - ClearDataDAO : ", err)
	result, err = db.Query(sql2)
	LogFatalf("Unable to reset increment - ClearDataDAO : ", err)

	sql = "DELETE FROM hcontext"
	sql2 = "DELETE FROM sqlite_sequence WHERE name='hcontext'"
	result2, err2 := db.Query(sql)
	LogFatalf("Unable to clear DB - ClearDataDAO : ", err2)
	result2, err2 = db.Query(sql2)
	LogFatalf("Unable to clear DB - ClearDataDAO : ", err2)

	logrus.Infof("Clear data results - hotkeys: %s", result)
	logrus.Infof("Clear data results: - hcontext %s", result2)
}
