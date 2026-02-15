pipeline {

    agent any

    stages {

        stage('Run ansible in check mode') {
            steps {
                sh 'ansible-galaxy collection install ansible.posix community.docker community.general'
                sh 'cd ansible && ansible-playbook site.yml --check'
            }
        }

    }
}
