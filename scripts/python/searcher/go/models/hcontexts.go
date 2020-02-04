package models

import (
	"time"

	. "github.com/instance-id/Searcher/utils"
	"github.com/sarulabs/di/v2"
)

type HContextAccessObject struct{}

type HContext struct {
	Id           int64     `xorm:"'id' pk autoincr notnull"`
	HCONTEXT     string    `xorm:"'hcontext' not null index(par_ind) VARCHAR(75)"`
	Context      string    `xorm:"'context' unique VARCHAR(75)"`
	Description  string    `xorm:"'description' VARCHAR(75)"`
	Title        string    `xorm:"'title' VARCHAR(75)"`
	LastModified time.Time `xorm:"'lastmodified' created"`
}

var HContextDAO *HContextAccessObject

func (h *HContextAccessObject) TableName() string {
	return "h_context"
}

// --- Create new hcontext object --------------------------------------------------------------------
func NewHContextObject(hcontext string, context string, description string, title string) *HContext {
	return &HContext{
		HCONTEXT:    hcontext,
		Context:     context,
		Description: description,
		Title:       title,
	}
}

// --- Add new user to database -------------------------------------------------------------------
func (h *HContextAccessObject) AddHContext(hcontext *HContext, di di.Container) {
	db := DatabaseAccessContainer(di)
	_, err := db.Table(HContextDAO.TableName()).InsertOne(hcontext)
	LogFatalf("Unable to insert hcontext", err)
	log := LogAccessContainer(di)
	log.Infof("Data from insert: %v", hcontext.Id)
}
