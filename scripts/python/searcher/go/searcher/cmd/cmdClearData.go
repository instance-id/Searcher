package cmd

import (
	"github.com/instance-id/Searcher/models"
	"github.com/sarulabs/di/v2"
)

type ClearData struct {
	di di.Container
}

const ClearDataRoute = "c"
const ClearDataDescription = "Clear current data from database"

func (t *ClearData) GetCommand() string {
	return ClearDataRoute
}

func (t *ClearData) GetDescription() string {
	return ClearDataDescription
}

func (t *ClearData) Handle() {
	models.ClearDataDAO.ClearData(t.di)
}

func NewClearData(di di.Container) *ClearData {
	return &ClearData{di: di}
}
