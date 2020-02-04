package cmd

import (
	"bytes"
	"fmt"

	"github.com/olekukonko/tablewriter"

	"github.com/instance-id/Searcher/models"
	"github.com/sarulabs/di/v2"
)

type QueryStatement struct {
	di di.Container
}

const QueryStatementRoute = "q"
const QueryStatementDescription = "Query SQL Statement"

func (q *QueryStatement) GetCommand() string {
	return QueryStatementRoute
}

func (q *QueryStatement) GetDescription() string {
	return QueryStatementDescription
}

func (q *QueryStatement) Handle(input string) {
	result := models.QueryStatementDAO.Query(q.di, input)
	table := q.renderMarkDownTable(result)
	resultTable := fmt.Sprintf("\n" + "```" + table + "```")
	fmt.Printf(resultTable)
	//fmt.Printf("result: %s\n", result[0]["assignments"])
	//fmt.Printf("result: %s\n", result)
	//fmt.Printf("result: %s\n", result[2])
}

func NewQueryStatement(di di.Container) *QueryStatement {
	return &QueryStatement{di: di}
}

func (q *QueryStatement) renderMarkDownTable(data []map[string][]byte) string {
	var tableData [][]string

	for k := range data {
		row := []string{
			string(data[k]["label"]),
			string(data[k]["description"]),
			string(data[k]["context"]),
			string(data[k]["assignments"]),
		}
		tableData = append(tableData, row)
	}

	//for k, v := range data {
	//	d := data[k]
	//	val := d[v]
	//	row := []string{[string(val)]}
	//	tableData = append(tableData, row)
	//}

	buffer := new(bytes.Buffer)

	table := tablewriter.NewWriter(buffer)
	table.SetHeader([]string{"Label:", "Description:", "Context:", "Assignment:"})
	table.SetColWidth(40)
	table.SetBorders(tablewriter.Border{Left: true, Top: false, Right: true, Bottom: false})
	table.SetCenterSeparator("|")
	table.AppendBulk(tableData)
	table.Render()

	return buffer.String()
}
