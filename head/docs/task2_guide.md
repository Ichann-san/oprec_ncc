========================================================
LOGPULSE MINI SIEM — TASK 2 DOCUMENTATION
CI/CD Pipeline (Jenkins + SonarQube)
========================================================

TABLE OF CONTENTS
--------------------------------------------------------
1. Task Overview
2. Requirements
3. Pipeline Architecture
4. Jenkinsfile Breakdown
5. SonarQube Configuration
6. Jenkins Setup Tutorial
7. SonarQube Setup Tutorial
8. GitHub Webhook Integration
9. Quality Gate Workflow
10. Troubleshooting
11. Screenshots

========================================================
1. TASK OVERVIEW
========================================================

Task 2 implements automated CI/CD using Jenkins and
code quality analysis using SonarQube.

Key deliverables:
  - Jenkinsfile with 8-stage declarative pipeline
  - SonarQube project configuration
  - Build, test, and deploy shell scripts
  - GitHub webhook trigger for auto-builds
  - Quality gate validation before deployment

Pipeline Goal:
  Every code push → automatically build, test,
  analyze code quality, and deploy if everything passes.

========================================================
2. REQUIREMENTS
========================================================

Services (running via docker-compose):
  - Jenkins (port 8080)
  - SonarQube (port 9000)

Jenkins Plugins:
  - Pipeline
  - SonarQube Scanner
  - Docker Pipeline
  - Git
  - JUnit

Tools on Jenkins agent:
  - Python 3.11+
  - Docker CLI
  - SonarQube Scanner
  - Git

========================================================
3. PIPELINE ARCHITECTURE
========================================================

  GitHub Push
      │
      ▼
  Jenkins Webhook Trigger
      │
      ▼
  ┌─────────────────────────────────┐
  │ Stage 1: Checkout               │
  │   Clone repo from GitHub        │
  ├─────────────────────────────────┤
  │ Stage 2: Install Dependencies   │
  │   Create venv, pip install      │
  ├─────────────────────────────────┤
  │ Stage 3: Run Tests              │
  │   pytest → JUnit XML report     │
  │      FAIL → Pipeline stops      │
  ├─────────────────────────────────┤
  │ Stage 4: SonarQube Analysis     │
  │   sonar-scanner scans app/      │
  ├─────────────────────────────────┤
  │ Stage 5: Quality Gate           │
  │   Wait for SonarQube result     │
  │      FAIL → Pipeline aborted    │
  ├─────────────────────────────────┤
  │ Stage 6: Build Docker Image     │
  │   docker build, tag latest      │
  ├─────────────────────────────────┤
  │ Stage 7: Deploy                 │
  │   docker compose down + up      │
  ├─────────────────────────────────┤
  │ Stage 8: Health Check           │
  │   curl /health → verify 200 OK  │
  │      FAIL → Deployment failed   │
  └─────────────────────────────────┘
      │
      ▼
  Pipeline Success OR Pipeline Failed

========================================================
4. JENKINSFILE BREAKDOWN
========================================================

Location: task2/jenkins/Jenkinsfile
Type: Declarative Pipeline

Environment Variables:
  DOCKER_IMAGE    = logpulse-backend
  DOCKER_TAG      = ${BUILD_NUMBER}
  SONAR_HOST_URL  = http://localhost:9000
  SONAR_PROJECT_KEY = logpulse-mini-siem
  APP_PORT        = 8000

Options:
  - timeout: 30 minutes max
  - timestamps: log timestamps
  - disableConcurrentBuilds: one build at a time
  - buildDiscarder: keep last 10 builds

Post Actions:
  - success: log success message
  - failure: log failure message
  - always: clean workspace

========================================================
5. SONARQUBE CONFIGURATION
========================================================

Location: task2/sonarqube/sonar-project.properties

Key Settings:
  Project Key:     logpulse-mini-siem
  Project Name:    LogPulse Mini SIEM
  Source Dir:       ../task1/backend/app
  Language:         Python 3.11
  Encoding:         UTF-8

Exclusions (not analyzed):
  - venv/**
  - __pycache__/**
  - static/**
  - templates/**
  - *.json
  - tests/**

Duplication Detection:
  Minimum tokens: 50
  Minimum lines: 5

Quality Gate Checks:
  - No new bugs
  - No new vulnerabilities
  - Maintainability rating: A
  - Duplicated lines < 3% on new code

========================================================
6. JENKINS SETUP TUTORIAL
========================================================

STEP 1: Access Jenkins for First Time
  1. Open http://SERVER_IP:8080
  2. Jenkins shows "Unlock Jenkins" page
  3. Get the initial admin password:

     docker exec logpulse-jenkins \
       cat /var/jenkins_home/secrets/initialAdminPassword

  4. Paste the password and click Continue
  5. Click "Install suggested plugins"
  6. Wait for plugin installation
  7. Create your admin user account
  8. Click "Save and Finish" → "Start using Jenkins"

  [INSERT SCREENSHOT: Jenkins unlock page]
  [INSERT SCREENSHOT: Plugin installation progress]
  [INSERT SCREENSHOT: Jenkins dashboard after setup]

STEP 2: Install Additional Plugins
  1. Go to Manage Jenkins → Plugins → Available plugins
  2. Search and install:
     - SonarQube Scanner
     - Docker Pipeline
  3. Restart Jenkins after installation

  [INSERT SCREENSHOT: Plugins installed]

STEP 3: Configure SonarQube Server in Jenkins
  1. Go to Manage Jenkins → System
  2. Scroll to "SonarQube servers" section
  3. Click "Add SonarQube"
  4. Fill in:
     - Name: SonarQube
     - Server URL: http://sonarqube:9000
     - Server authentication token: (from SonarQube — see Step 7)
  5. Click Save

  [INSERT SCREENSHOT: SonarQube server configuration in Jenkins]

STEP 4: Configure SonarQube Scanner Tool
  1. Go to Manage Jenkins → Tools
  2. Scroll to "SonarQube Scanner installations"
  3. Click "Add SonarQube Scanner"
  4. Fill in:
     - Name: SonarScanner
     - Check "Install automatically"
     - Version: latest
  5. Click Save

  [INSERT SCREENSHOT: SonarScanner tool configuration]

STEP 5: Create Pipeline Job
  1. On Jenkins dashboard → "New Item"
  2. Name: LogPulse-Pipeline
  3. Select "Pipeline" → OK
  4. In Pipeline section:
     - Definition: Pipeline script from SCM
     - SCM: Git
     - Repository URL: <your-github-repo-url>
     - Branch: */main
     - Script Path: head/task2/jenkins/Jenkinsfile
  5. Click Save

  [INSERT SCREENSHOT: Pipeline job configuration]
  [INSERT SCREENSHOT: SCM configuration with Jenkinsfile path]

STEP 6: Trigger First Build
  1. On the pipeline page, click "Build Now"
  2. Watch the build progress in the console output
  3. Each stage should turn green as it passes

  [INSERT SCREENSHOT: Pipeline stages all green]
  [INSERT SCREENSHOT: Build console output]

========================================================
7. SONARQUBE SETUP TUTORIAL
========================================================

STEP 1: Access SonarQube
  1. Open http://SERVER_IP:9000
  2. Default login: admin / admin
  3. SonarQube will ask you to change the password
  4. Set a new secure password

  [INSERT SCREENSHOT: SonarQube login page]
  [INSERT SCREENSHOT: SonarQube dashboard after login]

STEP 2: Create Project
  1. Click "Create Project" → "Manually"
  2. Fill in:
     - Project display name: LogPulse Mini SIEM
     - Project key: logpulse-mini-siem
     - Main branch name: main
  3. Click "Set Up"

  [INSERT SCREENSHOT: SonarQube project creation]

STEP 3: Generate Authentication Token
  1. Click your profile icon → My Account
  2. Go to "Security" tab
  3. Under "Generate Tokens":
     - Name: jenkins-token
     - Type: Project Analysis Token
     - Project: LogPulse Mini SIEM
  4. Click "Generate"
  5. COPY the token immediately (shown only once)
  6. Go back to Jenkins (Step 3 above) and paste this token

  [INSERT SCREENSHOT: Token generation page]

STEP 4: Configure Quality Gate
  1. Go to Quality Gates (top menu)
  2. The default "Sonar way" quality gate is applied
  3. This checks:
     - No new bugs
     - No new vulnerabilities
     - No new code smells rated worse than A
     - Duplicated lines < 3%
  4. You can create a custom gate if needed

  [INSERT SCREENSHOT: Quality gate configuration]

STEP 5: View Analysis Results
  After Jenkins runs the pipeline:
  1. Open the project in SonarQube
  2. Review:
     - Code Smells count
     - Bugs count
     - Vulnerabilities count
     - Duplicated lines %
     - Maintainability rating (A/B/C/D/E)
  3. Click into each category to see specific issues

  [INSERT SCREENSHOT: SonarQube analysis results overview]
  [INSERT SCREENSHOT: Code smells detail view]

========================================================
8. GITHUB WEBHOOK INTEGRATION
========================================================

Purpose: Auto-trigger Jenkins build on every git push.

STEP 1: Configure Jenkins Job for Webhook
  1. Open the LogPulse-Pipeline job → Configure
  2. Under "Build Triggers":
     - Check "GitHub hook trigger for GITScm polling"
  3. Save

STEP 2: Create GitHub Webhook
  1. Go to your GitHub repo → Settings → Webhooks
  2. Click "Add webhook"
  3. Fill in:
     - Payload URL: http://SERVER_IP:8080/github-webhook/
     - Content type: application/json
     - Secret: (leave empty or set a secret)
     - Events: Just the push event
  4. Click "Add webhook"

  [INSERT SCREENSHOT: GitHub webhook configuration]

STEP 3: Test the Webhook
  1. Push a commit to your repo
  2. Check Jenkins → the pipeline should trigger automatically
  3. Check GitHub webhook → should show a green checkmark

  [INSERT SCREENSHOT: Webhook delivery success in GitHub]
  [INSERT SCREENSHOT: Jenkins build triggered by webhook]

========================================================
9. QUALITY GATE WORKFLOW
========================================================

  Jenkins triggers SonarQube scan
      │
      ▼
  SonarQube analyzes app/ source code
      │
      ├── Checks code smells
      ├── Checks duplication
      ├── Checks bugs
      ├── Checks vulnerabilities
      ├── Checks maintainability rating
      │
      ▼
  Quality Gate Evaluation
      │
      ├── PASSED → Jenkins continues to Build & Deploy
      │
      └── FAILED → Jenkins pipeline ABORTED
                    Developer must fix issues and push again

========================================================
10. TROUBLESHOOTING
========================================================

Problem: Jenkins cannot connect to SonarQube
  Fix: Ensure both containers are on the same Docker
       network (logpulse-net). Use http://sonarqube:9000
       (Docker service name, not localhost).

Problem: SonarQube scanner not found
  Fix: In Jenkins → Manage Jenkins → Tools, ensure
       SonarQube Scanner is configured with auto-install.

Problem: Quality Gate timeout
  Fix: SonarQube may need time to process. Increase the
       timeout in the Jenkinsfile Quality Gate stage
       (default: 5 minutes).

Problem: Tests not found
  Fix: Ensure tests/ directory exists in head/task1/backend/
       with test_*.py files. The pipeline allows empty
       test results to avoid blocking.

Problem: Docker build fails in Jenkins
  Fix: Ensure Docker socket is accessible to Jenkins.
       The Jenkins container needs Docker CLI installed
       or Docker socket mounted.

========================================================
11. SCREENSHOTS
========================================================

Insert your screenshots below:

[INSERT SCREENSHOT: Jenkins dashboard with LogPulse pipeline]
[INSERT SCREENSHOT: Pipeline stages view (all green)]
[INSERT SCREENSHOT: Build console output]
[INSERT SCREENSHOT: SonarQube project overview]
[INSERT SCREENSHOT: SonarQube quality gate status]
[INSERT SCREENSHOT: GitHub webhook configured]
[INSERT SCREENSHOT: Auto-triggered build from webhook]

========================================================
END OF TASK 2 DOCUMENTATION
========================================================
