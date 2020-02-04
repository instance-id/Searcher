package main

import (
	"fmt"
	"os"
	"sort"

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

	log, appData := DISetup()
	defer appData.Delete()

	message := []string{
		"Starting Searcher"}
	for s := range message {
		msg := fmt.Sprintf("%s", message[s])
		log.Infof("%s", msg)
	}

	config := appData.Get("configData").(*appconfig.MainSettings)
	_, _ = appContext.Searcher.SearcherRun(config, appData)

	app := &cli.App{
		Flags: []cli.Flag{
			&cli.StringFlag{
				Name:  "lang, l",
				Value: "english",
				Usage: "Language for the greeting",
			},
			&cli.StringFlag{
				Name:  "config, c",
				Usage: "Load configuration from `FILE`",
			},
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
				// ----------------------------------------------------------------------------------------------------- cmdAddHContext
				Name: func() string {
					result := fmt.Sprintf((*cmd.AddHContext).GetCommand(cmd.NewAddHContext(appData)))
					return result
				}(),
				Aliases: []string{"addhcontext"},
				Usage: func() string {
					result := fmt.Sprintf((*cmd.AddHContext).GetDescription(cmd.NewAddHContext(appData)))
					return result
				}(),
				Action: func(c *cli.Context) error {
					(*cmd.AddHContext).Handle(cmd.NewAddHContext(appData))
					log.Infof("Add HContext Complete")
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
					log.Infof("Add HContext Complete")
					return nil
				},
			}, {
				// ----------------------------------------------------------------------------------------------------- cmdAddHotkeys
				Name: func() string {
					result := fmt.Sprintf((*cmd.QueryStatement).GetCommand(cmd.NewQueryStatement(appData)))
					return result
				}(),
				Aliases: []string{"querystatement"},
				Usage: func() string {
					result := fmt.Sprintf((*cmd.QueryStatement).GetDescription(cmd.NewQueryStatement(appData)))
					return result
				}(),
				Action: func(c *cli.Context) error {
					fmt.Printf("Query term: %s\n", c.Args().First())
					(*cmd.QueryStatement).Handle(cmd.NewQueryStatement(appData), c.Args().First())
					log.Infof("Querying")
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
	log := app.Get("logData").(*zap.SugaredLogger)

	return log, app
}
