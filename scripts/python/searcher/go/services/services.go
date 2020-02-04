package services

import (
	"github.com/instance-id/Searcher/appconfig"
	"github.com/instance-id/Searcher/components"
	. "github.com/instance-id/Searcher/utils"
	"github.com/sarulabs/di/v2"
	"go.uber.org/zap"
)

var Services = []di.Def{
	{
		Name:  "configData",
		Scope: di.App,
		Build: func(ctn di.Container) (interface{}, error) {
			var cfg appconfig.MainSettings
			config := cfg.GetConfig()
			return config, nil
		}},
	{
		// --- Get DB Data ----------------------------------------------------------------------
		Name:  "dbData",
		Scope: di.App,
		Build: func(ctn di.Container) (interface{}, error) {
			var db appconfig.DbSettings
			dbConfig := db.GetDbConfig()
			return dbConfig, nil
		}},
	{
		// --- Creates database connection object ----------------------------------------------------------------------
		Name:  "dbConn",
		Scope: di.App,
		Build: func(ctn di.Container) (interface{}, error) {
			var conn components.DbConfig
			dbconfig := ctn.Get("dbData").(*appconfig.DbSettings)
			dbConn := conn.ConnectDB(dbconfig)
			return dbConn, nil
		},
		Close: func(obj interface{}) error {
			return obj.(*components.DbConfig).Xorm.Close()
		},
	},
	{
		// --- Uses database connection object and returns a connection session ----------------------------------------
		Name:  "db",
		Scope: di.Request,
		Build: func(ctn di.Container) (interface{}, error) {
			conn := ctn.Get("dbConn").(*components.DbConfig).Xorm
			return conn, nil
		},
		Close: func(obj interface{}) error {
			return obj.(*components.DbConfig).Xorm.Close()
		},
	},
	{
		// ---Creates Zap to default DiscordGo logger ------------------------------------------------------------------
		Name: "logData",
		Build: func(ctn di.Container) (interface{}, error) {
			logger, err := zap.NewProduction()
			defer logger.Sync()
			ServicesError("Could not get new logger! ", err, logger.Sugar())

			log := logger.Sugar()
			return log, nil
		}},
}
