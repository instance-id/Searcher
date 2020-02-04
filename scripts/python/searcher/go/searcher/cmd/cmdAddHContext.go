package cmd

import (
	"github.com/instance-id/Searcher/models"
	"github.com/sarulabs/di/v2"
)

type AddHContext struct {
	di di.Container
}

const addHContextRoute = "ahc"
const addHContextDescription = "Add an HContext"

func (t *AddHContext) GetCommand() string {
	return addHContextRoute
}

func (t *AddHContext) GetDescription() string {
	return addHContextDescription
}

func (t *AddHContext) Handle() {
	hcontext := models.NewHContextObject("deskmgr", "deskmgr", "The Desktop Managers items", "Desktop Manager")
	models.HContextDAO.AddHContext(hcontext, t.di)
}

func NewAddHContext(di di.Container) *AddHContext {
	return &AddHContext{di: di}
}
