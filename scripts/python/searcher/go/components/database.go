package components

import (
	"github.com/instance-id/Searcher/appconfig"
	_ "github.com/mattn/go-sqlite3"
	"github.com/sirupsen/logrus"
	"xorm.io/xorm"
)

type DbConfig struct {
	Db   *appconfig.DbSettings
	Xorm *XormDB
}

type XormDB struct {
	Engine      *xorm.Engine
	dbChnl      chan dbQuery
	closeWorker chan error
	runit       bool
}

func (xdb *DbConfig) ConnectDB(d *appconfig.DbSettings) *DbConfig {
	dbConfig := &DbConfig{
		Db: d,
		Xorm: &XormDB{
			Engine: func() *xorm.Engine {
				eng, err := xorm.NewEngine(d.Database, d.DBLocation)
				if err != nil {
					logrus.Fatalf("Database Connection Error: %s", err)
				}
				return eng
			}(),
			dbChnl:      make(chan dbQuery, 32),
			closeWorker: make(chan error),
		},
	}
	return dbConfig
}

func (x *XormDB) Run() {
	for x.dbChnl != nil {
		ev, ok := <-x.dbChnl
		if !ok {
			break
		}
		ev.Query()
		ev.Done()
	}
	// close
	x.closeWorker <- x.Engine.Close()
	x.Engine = nil
}

func (x *XormDB) Close() (err error) {
	c := x.dbChnl
	x.dbChnl = nil
	close(c)
	err = <-x.closeWorker
	close(x.closeWorker)
	return
}
