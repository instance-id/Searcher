package utils

import (
	"github.com/instance-id/Searcher/appconfig"
	"github.com/instance-id/Searcher/components"
	"github.com/sarulabs/di/v2"
	"go.uber.org/zap"
	"xorm.io/xorm"

	Log "github.com/sirupsen/logrus"

)

var (
	Dba *xorm.Engine
	Dbd *appconfig.DbSettings
	Dac *appconfig.MainSettings
	//Log *zap.SugaredLogger
)

// --- Interfaces for container types -------------------------------------------------------------------------------------- TODO Probably remove if not used
type GetData interface {
	DataAccessContainer(di di.Container) *appconfig.MainSettings
	DatabaseAccessContainer(di di.Container) *xorm.Engine
	ErrCheckf(msg string, err error)
	Warnf(msg string, err error)
}

type ErrParam struct {
	Msg          string
	Err          error
	ShouldReturn bool
}

// --- Initialization of dependency injection containers from Verifier -----------------------------------------------------
func CmdInitialize(di di.Container) {
	Dac = DataAccessContainer(di)
	Dbd = DatabaseContainer(di)
	Dba = DatabaseAccessContainer(di)
	//Log = LogAccessContainer(di)

}

// --- Provides global access to configuration data via dependency injection container -------------------------------------
func DataAccessContainer(di di.Container) *appconfig.MainSettings {
	d, _ := di.Get("configData").(*appconfig.MainSettings)
	LogFatalf("Error accessing DI container within AddUser module: ", nil)
	return d
}

// --- Provides global access to configuration data via dependency injection container -------------------------------------
func DatabaseContainer(di di.Container) *appconfig.DbSettings {
	d, _ := di.Get("dbData").(*appconfig.DbSettings)
	return d
}

// --- Provides global database access via dependency injection container --------------------------------------------------
func DatabaseAccessContainer(di di.Container) *xorm.Engine {
	db, err := di.SubContainer()
	LogFatalf("Error accessing DI container from utils DatabaseAccessContainer(): ", err)

	database := db.Get("db").(*components.XormDB).Engine
	return database
}

// --- Provides global access to logger via dependency injection container -------------------------------------------------
func LogAccessContainer(di di.Container) *zap.SugaredLogger {
	l, _ := di.Get("logData").(*zap.SugaredLogger)
	LogFatalf("Error accessing DI container within AddUser module: ", nil)
	return l
}

// --- Error handling helper functions -------------------------------------------------------------------------------------
func InputWarn(msg string, err error) bool {
	if err != nil {
		Log.Warnf("%s %s", msg, err)
		return true
	}
	return false
}

func LogErrorRet(msg string, err error) bool {
	if err != nil {
		Log.Errorf("%s %s", msg, err)
		return true
	}
	return false
}

func LogErrorf(msg string, err error) {
	if err != nil {
		Log.Errorf("%s %s", msg, err)
	}
}

func LogErrorRetf(err *ErrParam) *ErrParam {
	if err.Err != nil {
		Log.Errorf("%s %s", err.Msg, err.Err)
		if err.ShouldReturn {
			return err
		}
		return nil
	}
	return nil
}

func LogFatalf(msg string, err error) {
	if err != nil {
		Log.Fatalf("%s %s", msg, err)
	}
}

func LogInfof(msg string, data interface{}) {
	if data != nil {
		Log.Infof("%v %v", msg, data)
	}
}

func LogWarnf(msg string, err error) {
	if err != nil {
		Log.Warnf("%s %s", msg, err)
	}
}

func ServicesError(msg string, err interface{}, logger *zap.SugaredLogger) {
	if err != nil {
		logger.Fatalf("%s %s", msg, err)
	}
}
