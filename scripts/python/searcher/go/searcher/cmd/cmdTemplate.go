package cmd

import (
	"github.com/sarulabs/di/v2"
)

type Template struct {
	di di.Container
}

const templateRoute = "template"
const templateDescription = "template"

func (t *Template) GetCommand() string {
	return dbSetupRoute
}

func (t *Template) GetDescription() string {
	return dbSetupDescription
}

func (t *Template) Handle() {

}

func NewTemplate(di di.Container) *Template {
	return &Template{di: di}
}
