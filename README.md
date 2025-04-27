# Nexus Python Demo

This project demonstrates how to publish and consume Python packages using a local Nexus repository.

## Project Structure

```
nexus-python-demo/
├── calculator/           # The calculator library
│   ├── calculator/       # Package directory
│   │   ├── __init__.py
│   │   └── calculator.py
│   └── setup.py
├── consumer/            # Consumer application
│   └── main.py
└── .pypirc             # Nexus configuration
```

## Prerequisites

- Python 3.6+
- Docker
- pip
- twine
- build
- curl

## Environment Variables

Create a `.env` file in the project root with the following variables:
```bash
NEXUS_URL=http://localhost:8081
NEXUS_USERNAME=admin
NEXUS_PASSWORD=your-password-here
```

## Docker Nexus Setup

1. Pull the Nexus image:
   ```bash
   docker pull sonatype/nexus3
   ```

2. Wait for Nexus to start (it may take 2-3 minutes). You can check the logs:
   ```bash
   docker logs -f nexus
   ```
   Look for the message: "Started Sonatype Nexus OSS"

3. Get the initial admin password:
   ```bash
   docker exec nexus cat /nexus-data/admin.password
   ```

4. Access Nexus web interface:
   - Open http://localhost:8081 in your browser
   - Login with username: `admin` and the password from step 5
   - Change the admin password when prompted

5. Configure Nexus for PyPI:
   - Click the gear icon (⚙️) in the top right
   - Go to "Security" > "Realms"
   - Move "Docker Bearer Token Realm" to the right column
   - Click "Save"

6. Create a PyPI hosted repository:
   - Click "Server Administration and Configuration" (⚙️)
   - Go to "Repositories"
   - Click "Create repository"
   - Select "pypi (hosted)"
   - Configure with these settings:
     - Name: pypi-hosted
     - Version policy: Release
     - Deployment policy: Allow redeploy
     - Click "Create repository"

## Setup

1. Install required tools:
   ```bash
   # Find your Python3 path
   which python3
   
   # Install build and twine
   python3 -m pip install build twine
   
   # Verify build is installed
   python3 -m pip show build
   ```

2. Verify Nexus is running:
   ```bash
   curl -u $NEXUS_USERNAME:$NEXUS_PASSWORD $NEXUS_URL/service/rest/v1/status
   ```

3. Configure your local environment:
   ```bash
   # Create .pypirc in your home directory
   cp .pypirc ~/.pypirc
   ```

## Publishing the Calculator Library

1. Navigate to the calculator directory:
   ```bash
   cd calculator
   ```

2. Build the package using the build tool:
   ```bash
   python3 -m build
   ```
   This will create both source distribution and wheel in the `dist` directory.

3. Upload to Nexus:
   ```bash
   python3 -m twine upload --repository nexus dist/*
   ```

4. Verify the package was uploaded:
   ```bash
   curl -u $NEXUS_USERNAME:$NEXUS_PASSWORD $NEXUS_URL/service/rest/v1/components?repository=pypi-hosted
   ```

## Consuming the Calculator Library

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Configure pip to use Nexus:
   ```bash
   # Create or update ~/.pip/pip.conf
   mkdir -p ~/.pip
   cat > ~/.pip/pip.conf << EOF
   [global]
   index-url = $NEXUS_URL/repository/pypi-hosted/simple
   trusted-host = localhost
   EOF
   ```

3. Install the package from Nexus:
   ```bash
   pip install calculator
   ```

4. Run the consumer application:
   ```bash
   cd consumer
   python main.py
   ```

## Troubleshooting

1. If you get authentication errors:
   ```bash
   # Verify your credentials
   curl -u $NEXUS_USERNAME:$NEXUS_PASSWORD $NEXUS_URL/service/rest/v1/status
   ```

2. If the repository is not accessible:
   ```bash
   # Check repository status
   curl -u $NEXUS_USERNAME:$NEXUS_PASSWORD $NEXUS_URL/service/rest/v1/repositories/pypi-hosted
   ```

3. If package upload fails:
   ```bash
   # Check Nexus logs
   docker logs nexus
   ```

4. If build fails:
   ```bash
   # Install build
   python3 -m pip install --upgrade build
   
   # Verify build installation
   python3 -m pip show build
   ```

5. If Nexus container fails to start:
   ```bash
   # Check if port 8081 is already in use
   lsof -i :8081
   
   # If needed, stop and remove the container
   docker stop nexus
   docker rm nexus
   
   # Start again with a different port
   docker run -d -p 8082:8081 --name nexus sonatype/nexus3
   ```

## Error Handling

The calculator library includes error handling for:
- Division by zero
- Invalid input types

The consumer application demonstrates how to handle these errors gracefully.

## Cleanup

To stop and remove the Nexus container while preserving data:
```bash
docker stop nexus
docker rm nexus
```

To completely remove Nexus and its data:
```bash
docker stop nexus
docker rm nexus
``` 