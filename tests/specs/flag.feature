Feature: Flag
	A feature flag to enable and disable features.

	Background:
		Given a feature flag named "flag0"

	Scenario: Enable the feature
		Given the flag is enabled
		Then the code should run

	Scenario: Disable the feature
		Given the flag is disabled
		Then the code should not run
