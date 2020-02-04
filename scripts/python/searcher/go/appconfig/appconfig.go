package appconfig

import (
	"github.com/gookit/config/v2"
	"github.com/gookit/config/v2/ini"
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

	hConfigLocation = "C:\\Users\\mosthated\\Documents\\houdini18.0\\Searcher\\searcher_config.ini"

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
