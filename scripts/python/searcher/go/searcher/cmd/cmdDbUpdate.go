package cmd

import (
	"fmt"

	. "github.com/instance-id/Searcher/utils"
	Log "github.com/sirupsen/logrus"

	"github.com/instance-id/Searcher/models"
	"github.com/sarulabs/di/v2"
)

type DbUpdate struct {
	di di.Container
}

const dbUpdateRoute = "du"
const dbUpdateDescription = "Database Update"

func (dbu *DbUpdate) GetCommand() string {
	return dbUpdateRoute
}

func (dbu *DbUpdate) GetDescription() string {
	return dbUpdateDescription
}

func (dbu *DbUpdate) Handle() {
	err := Dba.Sync2(new(models.Hcontext), new(models.Hotkeys))
	if err != nil {
		LogFatalf("Unable to send table creation reply through Discord: ", err)
	}

	resultv, err := Dba.IsTableExist("hcontext")
	LogFatalf(fmt.Sprintf("Verifier could not update table: verified_users : "), err)
	resultp, err := Dba.IsTableExist("hotkeys")
	LogFatalf(fmt.Sprintf("Verifier could not update table: user_packages : "), err)

	if resultv && resultp {
		Log.Infof("Schema applied: hcontext: %t - hotkeys: %t", resultv, resultp)
		Log.Infof("Database schema creation/update successful")
	}
}

func NewDbUpdate(di di.Container) *DbUpdate {
	return &DbUpdate{di: di}
}
