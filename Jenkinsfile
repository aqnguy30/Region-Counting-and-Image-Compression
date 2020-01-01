pipeline {
    agent { docker { image 'pmantini/assignment-cosc6380:latest' } }
    
    environment {
        PATH = "env/bin/:$PATH"
    }
    stages {
        stage('build') {
            steps {                
                sh 'python dip_hw2_region_analysis.py -i cells.png  > output/cellct/1/output.txt'                       
            }
        }                
    }
    post {
        always {
            archiveArtifacts artifacts: 'output/**/*.* ', onlyIfSuccessful: true
        }
    }
}
