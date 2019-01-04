def FAILED_STAGE = ""
def COMMITTER_EMAIL = ""
def COMMITTER_USER = ""
def BUILD_NAME
def BUILD_DES

pipeline {

    agent { label "main" }


    stages {
        stage('Init') {

            agent { label 'main' }

            steps {


                echo 'Pulling... :' + env.BRANCH_NAME


                script {
                    sh 'pwd'
                    sh 'printenv'

                    FAILED_STAGE = env.STAGE_NAME

                    COMMITTER_EMAIL = sh(
                            script: 'git --no-pager show -s --format=\'%ae\'',
                            returnStdout: true).trim()

                    COMMITTER_USER = sh(
                            script: 'git --no-pager show -s --format=\'%cn\'',
                            returnStdout: true).trim()

                    BUILD_DES = "${COMMITTER_USER} - ${env.BRANCH_NAME}"
                    BUILD_NAME = "#${env.BUILD_NUMBER} - Jenkins"
                    bitbucketStatusNotify(buildState: 'INPROGRESS', buildName: BUILD_NAME, buildDescription: BUILD_DES)

                    echo "COMMITTER_EMAIL:${COMMITTER_EMAIL}"
                    echo "COMMITTER_USER:${COMMITTER_USER}"
                }
            }
        }
        stage('ScanSonar') {
            agent {
                label 'main'
            }
            steps {

                sh 'pwd'
                script {

                    FAILED_STAGE = env.STAGE_NAME

                    echo "Inicializando sonar"

                    def scanner = tool 'SonarScanner';

                    withSonarQubeEnv('SonarQube_main') {
                        echo "Sonar scanner path: " + scanner
                        sh "${scanner}/bin/sonar-scanner -X"
                    }
                }

                echo "Analisis terminado"
            }
        }
        stage('Quality Gate') {

            agent {
                label 'main'
            }

            options {
                timeout(time: 5, unit: 'MINUTES')

            }

            steps {


                script {

                    FAILED_STAGE = env.STAGE_NAME
                    sleep(1)

                    echo "Esperando resultado de quality gate..."

                    def qg = waitForQualityGate()

                    echo "El estado del Quality Gate es: ${qg.status}"

                    if (qg.status != 'OK') {
                        echo "Pipeline cancelado no cumple el Quaity Gate. EstadoSonar=${qg.status}"
                        sh 'exit 1'
                    }

                }
            }
        }
        stage('Deploy') {
            agent {
                label 'web'
            }
            steps {
                script {
                    FAILED_STAGE = env.STAGE_NAME
                }

                sh 'pwd'
                sh 'whoami'
                sh 'git --git-dir=/home/akzio/www/src/.git --work-tree=/home/akzio/www/src pull'
                sh 'JENKINS_NODE_COOKIE=dontKillMe /home/akzio/www/server/start.sh'
            }
        }
        stage('Check Deploy') {
            agent {
                label 'main'
            }
            options {
                timeout(time: 4, unit: 'MINUTES')

            }
            steps {
                script {
                    FAILED_STAGE = env.STAGE_NAME
                    sleep(5)
                    try {
                        def result = sh(returnStdout: true, script: 'curl 10.0.20.146:8080 | grep -i preguntas | wc -l').trim()
                        echo "Check Deploy Result: ${result}"
                        if (result == "0") {
                            echo "Check Site: Error"
                            currentBuild.result = 'FAILURE'
                            error "El sitio no esta deployado correctamente"
                            return false
                        } else {
                            echo "Check Site: true"
                            return true
                        }


                    } catch (Exception e) {
                        echo "Check Site: False"
                        currentBuild.result = 'FAILURE'
                        error "El sitio no esta deployado correctamente"
                        return false
                    }
                }

            }
        }
    }
    post {
        always {

            echo 'Post: always Jenkins'
            echo "COMMITTER_EMAIL:${COMMITTER_EMAIL}"
            echo "COMMITTER_USER:${COMMITTER_USER}"
        }

        success {
            node('main') {
                script {
                    echo 'Post: Success'
                    BUILD_DES = "${BUILD_DES}"
                    bitbucketStatusNotify(buildState: 'SUCCESSFUL', buildName: BUILD_NAME, buildDescription: BUILD_DES)

                    emailext body: """<p>SUCCESS ${BUILD_DES}: '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
        <p>Comprueba la consola de salida;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a></p>""",
                            subject: "SUCCESS ${BUILD_DES}: 'Jenkinns #:[${env.BUILD_NUMBER}]'",
                            recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']], to: 'alexander.volantines@akzio.cl, steven.delgado@akzio.cl, oraima.garcia@akzio.cl, yurisan.collado@akzio.cl'

                }
            }
        }

        failure {
            node('main') {
                script {
                    echo "Post: Fallo en el Stage: ${FAILED_STAGE}"
                    BUILD_DES = "${BUILD_DES} - Etapa:${FAILED_STAGE}"
                    bitbucketStatusNotify(buildState: 'FAILED', buildName: BUILD_NAME, buildDescription: BUILD_DES)


                    emailext body: """<p>Failure ${BUILD_DES}, ${env.JOB_NAME} [${env.BUILD_NUMBER}]:</p>
        <p>Comprueba la consola de salida;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a></p>""",
                            subject: "Failure ${BUILD_DES}: 'Jenkinns #:[${env.BUILD_NUMBER}]'",
                            recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']], to: 'alexander.volantines@akzio.cl, steven.delgado@akzio.cl, oraima.garcia@akzio.cl, yurisan.collado@akzio.cl '

                }
            }
        }

        aborted {
            node('main') {
                script {

                    echo "Post: Abortado en el Stage: ${FAILED_STAGE}"
                    BUILD_DES = "${BUILD_DES} - Etapa:${FAILED_STAGE}"
                    bitbucketStatusNotify(buildState: 'FAILED', buildName: BUILD_NAME, buildDescription: BUILD_DES)

                    emailext body: """<p>Aborted ${BUILD_DES},  ${env.JOB_NAME} [${env.BUILD_NUMBER}]:</p>
        <p>Comprueba la consola de salida;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a></p>""",
                            subject: "Aborted ${BUILD_DES}: 'Jenkinns #:[${env.BUILD_NUMBER}]'",
                            recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']], to: 'alexander.volantines@akzio.cl, steven.delgado@akzio.cl, oraima.garcia@akzio.cl, yurisan.collado@akzio.cl'

                }
            }
        }

        unstable {
            node('main') {
                script {
                    echo 'Post: unstable'
                    BUILD_DES = "${BUILD_DES} - Unstable:${FAILED_STAGE}"
                    bitbucketStatusNotify(buildState: 'FAILED', buildName: BUILD_NAME, buildDescription: BUILD_DES)
                }
            }
        }

        changed {
            node('main') {
                script {
                    echo 'Post: changed'
                    //BUILD_DES = "${BUILD_DES} - Changed:${FAILED_STAGE}"
                    //bitbucketStatusNotify(buildState: 'FAILED', buildName: BUILD_NAME, buildDescription: BUILD_DES)
                }
            }
        }

    }
}