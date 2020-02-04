package appconfig

import (
	"github.com/gookit/config/v2"
	"github.com/gookit/config/v2/ini"
)

// --- Maps dbconfig.yml fields to DbSettings fields -------------------------------------------------------------------
type DbSettings struct {
	Database   string `json:"database"`
	DBLocation string `json:"dblocation"`
}

// --- Gets called from Services and returns DbSettings to Dependency Injection container ------------------------------
func (d *DbSettings) GetDbConfig() *DbSettings {
	return d.loadDbConfig()
}

// --- Populates the DbSettings struct from dbconfig.yml file and returns the data for use -----------------------------
func (d *DbSettings) loadDbConfig() *DbSettings {
	config.AddDriver(ini.Driver)
	filename := "../config/dbconfig.ini"

	err := config.LoadFiles(filename)
	if err != nil {
		panic(err)
	}

	dbSettings := &DbSettings{
		Database:   config.String("database"),
		DBLocation: config.String("dblocation"),
	}
	return dbSettings
}
