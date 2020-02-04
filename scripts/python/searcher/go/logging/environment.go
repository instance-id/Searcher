package logging

// Environment represents a environment in which a service is running
type Environment string

// defines possibly environments
const (
	DevelopmentEnvironment Environment = "development"
	ProductionEnvironment  Environment = "production"
	OutputEnvironment      Environment = "output"
)
