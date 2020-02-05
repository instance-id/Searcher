package appconfig

import (
	"github.com/gookit/config/v2"
	"github.com/gookit/config/v2/ini"
	"github.com/sirupsen/logrus"
	"os"
	"os/user"
	"path/filepath"
)

type ConfigData struct {
	MainSettings MainSettings
}

var hConfigLocation string

type MainSettings struct {
	Houdini struct {
		HoudiniConfig string `json:"houdiniconfig"`
	} `json:"houdini"`
	Searcher struct {
		Option1 string `json:"option1"`
	} `json:"searcher"`
}

func (m *MainSettings) GetConfig() *MainSettings {
	return m.loadConfig()
}

func (m *MainSettings) loadConfig() *MainSettings {

	hpath := os.Getenv("HOUDINI_USER_PREF_DIR")
	if len(hpath) == 0 {
		userData, err := user.Current()
		if err != nil {
			logrus.Errorf("Could not get current user data: %s", err)
		}
		hConfigLocation = filepath.Join(userData.HomeDir, "Documents", "houdini18.0", "Searcher", "searcher_config.ini")
	} else {
		hConfigLocation = filepath.Join(hpath, "Searcher", "searcher_config.ini")
	}

	config.AddDriver(ini.Driver)
	filename := hConfigLocation

	err := config.LoadFiles(filename)
	if err != nil {
		panic(err)
	}

	mainSettings := &MainSettings{
		Houdini: struct {
			HoudiniConfig string `json:"houdiniconfig"`
		}{
			HoudiniConfig: config.String("houdini.houdiniconfig"),
		},
		Searcher: struct {
			Option1 string `json:"option1"`
		}{
			Option1: config.String("searcher.option1"),
		}}

	return mainSettings
}
