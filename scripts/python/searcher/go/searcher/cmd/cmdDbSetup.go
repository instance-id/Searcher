package cmd

import (
	. "github.com/instance-id/Searcher/utils"

	"github.com/instance-id/Searcher/models"

	"github.com/sarulabs/di/v2"
)

type DbSetup struct {
	di di.Container
}

const dbSetupRoute = "ds"
const dbSetupDescription = "Database Setup"

func (ds *DbSetup) GetCommand() string {
	return dbSetupRoute
}

func (ds *DbSetup) GetDescription() string {
	return dbSetupDescription
}

func (ds *DbSetup) Handle() {
	d := DatabaseAccessContainer(ds.di)

	if !(func() bool { value, _ := d.IsTableExist("hcontext"); return value }() &&
		func() bool { value, _ := d.IsTableExist("hotkeys"); return value }()) {
		Log.Infow("Database schema incomplete. Creating/Updating table schema now...")

		err := d.Sync(new(models.HContext), new(models.Hotkeys))
		if err != nil {
			Log.Infow("Verifier was unable to create tables: %s", err)
		}

		resultv, err := d.IsTableExist("hcontext")
		resultp, err := d.IsTableExist("hotkeys")
		if err != nil {
			Log.Errorf("Error: %t", err)
		}

		if resultp && resultv {
			Log.Infow("Schema applied: hcontext: %t - hotkeys: %t", resultv, resultp)
		}

		Log.Infow("Database schema creation/update successful")

	} else {
		Log.Infow("Database schema already up to date")
	}
}

func NewDbSetup(di di.Container) *DbSetup {
	return &DbSetup{di: di}
}
