package components

type dbQuery interface {
	// Do the Db query for this event
	Query()
	// Get any errors that happened
	Error() error
	// Wait for this query to complete
	Wait()
	// Called when query is done
	Done()
}

type dbEvent struct {
	X *XormDB
	// Completetion channel
	chnl chan bool
}

func (ev *dbEvent) Wait() {
	<-ev.chnl
	close(ev.chnl)
}

func (ev *dbEvent) Done() {
	ev.chnl <- true
}
