def quick_build(def cov_option) {
	return [
		stage('linting') {
			sh "tox -e linting"
		},
		stage('security') {
			sh "tox -e security"
		},
		stage('unit tests') {
			sh '''
				tox -e pypy3-${cov_option} -- -m unit || error=true
				tox -e py36-${cov_option} -- -m unit || error=true

				if [ $error ]
				then
					exit 1
				fi
			'''
		}
	]
}

def full_build() {
	def stages = quick_build("cov")
	stages.push(
		stage('integration tests') {
			sh '''
				tox -e pypy3-cov -- -m integration || error=true
				tox -e py36-cov -- -m integration || error=true

				if [ $error ]
				then
					exit 1
				fi
			'''
		}
	)

	stages.push(
		stage('e2e tests') {
			sh '''
				tox -e pypy3-cov -- -m e2e || error=true
				tox -e py36-cov -- -m e2e || error=true

				if [ $error ]
				then
					exit 1
				fi
			'''
		}
	)

	stages.push(
		stage('coverage report') {
			sh "tox -e coverage-report"
		}
	)

	return stages
}

properties([
	pipelineTriggers([
		cron('H */3 * * *'),
		pollSCM('H/5 * * * *')
	])
])

branch = env.BRANCH_NAME
def timerTrigger = currentBuild.rawBuild.getCause(hudson.triggers.TimerTrigger$TimerTriggerCause)

node() {
	checkout scm

	switch(branch) {
		case 'master':
			if (!timerTrigger) {
				full_build()

				stage('build package') {
					sh "tox -e wheel"
				}
			}
			break

		case 'develop':
			if (timerTrigger) {
				full_build()
			}
			break
		default:
			if (!timerTrigger) {
				quick_build("without coverage")
			}
	}
}
