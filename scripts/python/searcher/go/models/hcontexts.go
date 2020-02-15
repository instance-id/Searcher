package models

import (
	"time"

	. "github.com/instance-id/Searcher/utils"
	"github.com/sarulabs/di/v2"
)

type HcontextAccessObject struct{}

type Hcontext struct {
	Id           int64     `xorm:"'id' pk autoincr notnull"`
	Context      string    `xorm:"'context' unique not null index(par_ind) VARCHAR(75)"`
	Description  string    `xorm:"'description' VARCHAR(75)"`
	Title        string    `xorm:"'title' VARCHAR(75)"`
	LastModified time.Time `xorm:"'lastmodified' created"`
}

var HcontextDAO *HcontextAccessObject

func (h *HcontextAccessObject) TableName() string {
	return "hcontext"
}

// --- Create new hcontext object --------------------------------------------------------------------
func NewHcontextObject(context string, description string, title string) *Hcontext {
	return &Hcontext{
		Context:     context,
		Description: description,
		Title:       title,
	}
}

// --- Add new user to database -------------------------------------------------------------------
func (h *HcontextAccessObject) AddHcontext(hcontext *Hcontext, di di.Container) {
	db := DatabaseAccessContainer(di)
	_, err := db.Table(HcontextDAO.TableName()).InsertOne(hcontext)
	LogFatalf("Unable to insert hcontext", err)
	log := LogAccessContainer(di)
	log.Infof("Data from insert: %v", hcontext.Id)
}
