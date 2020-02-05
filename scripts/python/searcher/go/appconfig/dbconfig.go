package appconfig

import (
	"github.com/gookit/config/v2"
	"github.com/gookit/config/v2/ini"
	"github.com/sirupsen/logrus"
	"os"
	"path/filepath"
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
	path := os.Getenv("SEARCHER")
	if len(path) == 0 {
		path = filepath.Join("../config", "dbconfig.ini")
	} else {
		path = filepath.Join(path, "scripts", "python", "searcher", "config", "dbconfig.ini")
	}

	config.AddDriver(ini.Driver)
	filename := path

	err := config.LoadFiles(filename)
	if err != nil {
		logrus.Errorf("Could not load dbconfig.ini: %s", err)
	}

	dbSettings := &DbSettings{
		Database:   config.String("database"),
		DBLocation: config.String("dblocation"),
	}
	return dbSettings
}
