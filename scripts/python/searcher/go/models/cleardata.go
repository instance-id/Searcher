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

	sql := ("DELETE FROM hotkeys")
	result, err := db.Query(sql)
	LogFatalf("Unable to clear DB - ClearDataDAO : ", err)

	sql = ("DELETE FROM h_context")
	result2, err2 := db.Query(sql)
	LogFatalf("Unable to clear DB - ClearDataDAO : ", err2)

	logrus.Infof("Clear data results - hotkeys: %s", result)
	logrus.Infof("Clear data results: - hcontext %s", result2)
}
