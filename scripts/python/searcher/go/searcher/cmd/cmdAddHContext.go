package cmd

import (
	"github.com/instance-id/Searcher/models"
	"github.com/sarulabs/di/v2"
)

type AddHcontext struct {
	di di.Container
}

const addHcontextRoute = "ahc"
const addHcontextDescription = "Add an Hcontext"

func (t *AddHcontext) GetCommand() string {
	return addHcontextRoute
}

func (t *AddHcontext) GetDescription() string {
	return addHcontextDescription
}

func (t *AddHcontext) Handle() {
	hcontext := models.NewHcontextObject("deskmgr", "The Desktop Managers items", "Desktop Manager")
	models.HcontextDAO.AddHcontext(hcontext, t.di)
}

func NewAddHcontext(di di.Container) *AddHcontext {
	return &AddHcontext{di: di}
}
