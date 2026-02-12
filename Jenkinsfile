pipeline {
    agent any

    stages {
        stage('Run ansible in check mode') {
            steps {
                echo 'Step 1'
                cd ansible
                echo 'Step 2'
                sh 'ansible-playbook site.yml --check'
            }
        }
        stage('Stage II') {
            steps {
                echo 'Step A'
                echo 'Step B'
            }
        }
    }
}

/*
node {
    echo 'Hello, Jenkins!'
}
*/
