package main

import (
	"fmt"

	"github.com/blevesearch/bleve"
)

func main() {
	// open a new index
	mapping := bleve.NewIndexMapping()
	index, err := bleve.New("example.bleve", mapping)

	// index some data
	err = index.Index("id", "db.json")

	// search for some text
	query := bleve.NewMatchQuery("text")
	search := bleve.NewSearchRequest(query)
	searchResults, err := index.Search(search)
	fmt.Println(searchResults)
}
