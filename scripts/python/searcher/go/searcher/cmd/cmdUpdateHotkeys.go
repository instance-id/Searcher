package cmd

import (
	"github.com/instance-id/Searcher/models"
	"github.com/sarulabs/di/v2"
)

type AddHotkeys struct {
	di di.Container
}

const AddHotkeysRoute = "ahk"
const AddHotkeysDescription = "Add an HContext"

func (t *AddHotkeys) GetCommand() string {
	return AddHotkeysRoute
}

func (t *AddHotkeys) GetDescription() string {
	return AddHotkeysDescription
}

func (t *AddHotkeys) Handle(method string) {
	models.HotkeysDAO.AddAllHotkeys(t.di, method)
}

func NewAddHotkeys(di di.Container) *AddHotkeys {
	return &AddHotkeys{di: di}
}
