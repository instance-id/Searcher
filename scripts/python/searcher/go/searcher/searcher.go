package searcher

import (
	. "github.com/instance-id/Searcher/utils"

	"github.com/instance-id/Searcher/appconfig"
	"github.com/instance-id/Searcher/searcher/cmd"
	"github.com/sarulabs/di/v2"
	"go.uber.org/zap"
)

type Searcher struct{}

var log *zap.SugaredLogger

type Config struct {
	Settings *appconfig.MainSettings
	di       di.Container
	Routes   []cmd.Route
}

func (v *Searcher) SearcherRun(s *appconfig.MainSettings, di di.Container) (*Config, error) {
	log = di.Get("logData").(*zap.SugaredLogger)
	CmdInitialize(di)

	settings := &Config{Settings: s,
		di: di,
		Routes: []cmd.Route{
			cmd.NewDbSetup(di),
			cmd.NewDbUpdate(di)}}

	return settings, nil
}
