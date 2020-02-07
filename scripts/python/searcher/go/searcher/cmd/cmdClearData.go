package cmd

import (
	"github.com/instance-id/Searcher/models"
	"github.com/sarulabs/di/v2"
)

type AddHotkeys struct {
	di di.Container
}

const AddHotkeysRoute = "ahk"
const AddHotkeysDescription = "Add all hotkeys to database"

func (t *AddHotkeys) GetCommand() string {
	return AddHotkeysRoute
}

func (t *AddHotkeys) GetDescription() string {
	return AddHotkeysDescription
}

func (t *AddHotkeys) Handle() {
	models.HotkeysDAO.ProcessHotkeys(t.di, "insert")
}

func NewAddHotkeys(di di.Container) *AddHotkeys {
	return &AddHotkeys{di: di}
}
