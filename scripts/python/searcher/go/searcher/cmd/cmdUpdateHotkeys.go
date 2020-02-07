package cmd

import (
	"github.com/instance-id/Searcher/models"
	"github.com/sarulabs/di/v2"
)

type UpdateHotkeys struct {
	di di.Container
}

const UpdateHotkeysRoute = "uhk"
const UpdateHotkeysDescription = "Parse configs and update current hotkey data"

func (t *UpdateHotkeys) GetCommand() string {
	return UpdateHotkeysRoute
}

func (t *UpdateHotkeys) GetDescription() string {
	return UpdateHotkeysDescription
}

func (t *UpdateHotkeys) Handle() {
	models.HotkeysDAO.ProcessHotkeys(t.di, "update")
}

func NewUpdateHotkeys(di di.Container) *UpdateHotkeys {
	return &UpdateHotkeys{di: di}
}
