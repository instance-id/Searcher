package main

import (
	"fmt"
	"os"
	"sort"

	log "github.com/sirupsen/logrus"

	"github.com/instance-id/Searcher/searcher/cmd"

	"github.com/instance-id/Searcher/appconfig"

	"github.com/sarulabs/di/v2"
	"go.uber.org/zap"

	"github.com/instance-id/Searcher/searcher"
	"github.com/instance-id/Searcher/services"

	"github.com/cockroachdb/errors"
	"github.com/urfave/cli/v2"
)

var commands []cmd.Route

type appContext struct {
	Searcher *searcher.Searcher
}

func init() {

}

func main() {
	var appContext appContext

	_, appData := DISetup()
	defer appData.Delete()

	config := appData.Get("configData").(*appconfig.MainSettings)
	_, _ = appContext.Searcher.SearcherRun(config, appData)

	var datastring string

	app := &cli.App{
		Flags: []cli.Flag{
			// --- Query term --------------------------------------------------------------------------
			&cli.StringFlag{
				Name: func() string {
					result := fmt.Sprintf((*cmd.QueryStatement).GetCommand(cmd.NewQueryStatement(appData)))
					return result
				}(),
				Value: "",
				Usage: func() string {
					result := fmt.Sprintf((*cmd.QueryStatement).GetDescription(cmd.NewQueryStatement(appData)))
					return result
				}(),
				Destination: &datastring,
			},
		},
		Action: func(c *cli.Context) error {
			if c.NArg() > 0 {
				datastring = c.Args().Get(0)
			}

			if c.IsSet(func() string { // --- Query database for term ----------------------------------
				result := fmt.Sprintf((*cmd.QueryStatement).GetCommand(cmd.NewQueryStatement(appData)))
				return result
			}()) {
				(*cmd.QueryStatement).Handle(cmd.NewQueryStatement(appData), datastring)
			}
			return nil
		},
		Commands: []*cli.Command{
			{
				// ----------------------------------------------------------------------------------------------------- cmdDbSetup
				Name: func() string {
					result := fmt.Sprintf((*cmd.DbSetup).GetCommand(cmd.NewDbSetup(appData)))
					return result
				}(),
				Aliases: []string{"dbsetup"},
				Usage: func() string {
					result := fmt.Sprintf((*cmd.DbSetup).GetDescription(cmd.NewDbSetup(appData)))
					return result
				}(),
				Action: func(c *cli.Context) error {
					(*cmd.DbSetup).Handle(cmd.NewDbSetup(appData))
					log.Infof("DB Setup Complete")
					return nil
				},
			}, {
				// ----------------------------------------------------------------------------------------------------- cmdDbUpdate
				Name: func() string {
					result := fmt.Sprintf((*cmd.DbUpdate).GetCommand(cmd.NewDbUpdate(appData)))
					return result
				}(),
				Aliases: []string{"dbupdate"},
				Usage: func() string {
					result := fmt.Sprintf((*cmd.DbUpdate).GetDescription(cmd.NewDbUpdate(appData)))
					return result
				}(),
				Action: func(c *cli.Context) error {
					(*cmd.DbUpdate).Handle(cmd.NewDbUpdate(appData))
					log.Infof("DB Update Complete")
					return nil
				},
			}, {
				// ----------------------------------------------------------------------------------------------------- cmdClearData
				Name: func() string {
					result := fmt.Sprintf((*cmd.ClearData).GetCommand(cmd.NewClearData(appData)))
					return result
				}(),
				Aliases: []string{"cleardata"},
				Usage: func() string {
					result := fmt.Sprintf((*cmd.ClearData).GetDescription(cmd.NewClearData(appData)))
					return result
				}(),
				Action: func(c *cli.Context) error {
					(*cmd.ClearData).Handle(cmd.NewClearData(appData))
					log.Infof("Cleared data")
					return nil
				},
			}, {
				// ----------------------------------------------------------------------------------------------------- cmdAddHotkeys
				Name: func() string {
					result := fmt.Sprintf((*cmd.AddHotkeys).GetCommand(cmd.NewAddHotkeys(appData)))
					return result
				}(),
				Aliases: []string{"addhotkeys"},
				Usage: func() string {
					result := fmt.Sprintf((*cmd.AddHotkeys).GetDescription(cmd.NewAddHotkeys(appData)))
					return result
				}(),
				Action: func(c *cli.Context) error {
					(*cmd.AddHotkeys).Handle(cmd.NewAddHotkeys(appData))
					log.Infof("Hotkeys added")
					return nil
				},
			}, {
				// ----------------------------------------------------------------------------------------------------- cmdUpdateHotkeys
				Name: func() string {
					result := fmt.Sprintf((*cmd.UpdateHotkeys).GetCommand(cmd.NewUpdateHotkeys(appData)))
					return result
				}(),
				Aliases: []string{"updatehotkeys"},
				Usage: func() string {
					result := fmt.Sprintf((*cmd.UpdateHotkeys).GetDescription(cmd.NewUpdateHotkeys(appData)))
					return result
				}(),
				Action: func(c *cli.Context) error {
					(*cmd.UpdateHotkeys).Handle(cmd.NewUpdateHotkeys(appData))
					log.Infof("Hotkeys updated")
					return nil
				},
			},
		},
	}

	sort.Sort(cli.FlagsByName(app.Flags))
	sort.Sort(cli.CommandsByName(app.Commands))

	errors.Wrap(app.Run(os.Args), "Error: ")
}

func DISetup() (*zap.SugaredLogger, di.Container) {
	builder, _ := di.NewBuilder()
	_ = builder.Add(services.Services...)
	app := builder.Build()
	log1 := app.Get("logData").(*zap.SugaredLogger)

	return log1, app
}
