package cmd

type Route interface {
	GetCommand() string
	GetDescription() string
}

type DefaultRouteHandler interface {
	Handle()
}

type SubRoute interface {
	Route
	GetSubRoutes() []Route
}
