# Task 2 — CI/CD (Jenkins + SonarQube)

## Overview
Automated build, test, analyze, and deploy pipeline using Jenkins with SonarQube code quality integration.

## Pipeline Flow
```
GitHub Push
    |
    v
Jenkins Trigger (webhook)
    |
    +---- Install Dependencies
    |
    +---- Run Tests (pytest)
    |
    +---- SonarQube Scan
    |
    +---- Quality Gate Check
    |
    +---- Build Docker Image
    |
    +---- Deploy Containers
    |
    +---- Health Check
```

## Files

### Jenkins
| File | Purpose |
|------|---------|
| `jenkins/Jenkinsfile` | Declarative pipeline with 8 stages |
| `jenkins/pipeline/build_stage.txt` | Build stage documentation |
| `jenkins/pipeline/test_stage.txt` | Test stage documentation |
| `jenkins/pipeline/analyze_stage.txt` | SonarQube analysis documentation |
| `jenkins/pipeline/deploy_stage.txt` | Deploy stage documentation |

### SonarQube
| File | Purpose |
|------|---------|
| `sonarqube/sonar-project.properties` | Scanner configuration |

### Scripts
| File | Purpose |
|------|---------|
| `scripts/build.sh` | Build Docker image |
| `scripts/test.sh` | Run pytest suite |
| `scripts/deploy.sh` | Deploy via Docker Compose |

## Jenkins Setup Tutorial

### Step 1: Access Jenkins
1. After running `docker compose up -d`, open http://localhost:8080
2. First-time setup: get the initial admin password:
   ```powershell
   docker exec logpulse-jenkins cat /var/jenkins_home/secrets/initialAdminPassword
   ```
3. Paste the password and follow the setup wizard
4. Install suggested plugins

### Step 2: Install Required Plugins
Go to **Manage Jenkins → Plugins → Available** and install:
- **Pipeline** (usually pre-installed)
- **SonarQube Scanner**
- **Docker Pipeline**
- **Git**

### Step 3: Configure SonarQube in Jenkins
1. Go to **Manage Jenkins → System**
2. Scroll to **SonarQube Servers**
3. Click **Add SonarQube**
   - Name: `SonarQube`
   - Server URL: `http://sonarqube:9000` (Docker network name)
   - Authentication token: (generate from SonarQube — see Step 5)

### Step 4: Configure SonarQube Scanner
1. Go to **Manage Jenkins → Tools**
2. Scroll to **SonarQube Scanner**
3. Click **Add SonarQube Scanner**
   - Name: `SonarScanner`
   - Check "Install automatically"

### Step 5: Set Up SonarQube Project
1. Open http://localhost:9000
2. Default login: **admin / admin** (change on first login)
3. Create a new project:
   - Project key: `logpulse-mini-siem`
   - Display name: `LogPulse Mini SIEM`
4. Generate a token:
   - Go to **My Account → Security → Generate Token**
   - Name: `jenkins-token`
   - Copy the token — paste it in Jenkins (Step 3)

### Step 6: Create Jenkins Pipeline
1. In Jenkins: **New Item → Pipeline**
2. Name: `LogPulse-Pipeline`
3. Under **Pipeline**:
   - Definition: **Pipeline script from SCM**
   - SCM: **Git**
   - Repository URL: your GitHub repo URL
   - Script Path: `head/task2/jenkins/Jenkinsfile`
4. Save and click **Build Now**

### Step 7: Configure GitHub Webhook (Optional)
1. In GitHub repo: **Settings → Webhooks → Add webhook**
2. Payload URL: `http://YOUR_SERVER_IP:8080/github-webhook/`
3. Content type: `application/json`
4. Events: Just the push event
5. In Jenkins job: check **GitHub hook trigger for GITScm polling**

## Pipeline Failure Conditions
The pipeline will FAIL and stop if:
- Any pytest test fails
- SonarQube Quality Gate fails
- Docker build fails
- Health check fails after deployment
