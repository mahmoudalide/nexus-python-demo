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
- Docker (for running Nexus)
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

2. Start Nexus using Docker:
   ```bash
   docker run -d -p 8081:8081 --name nexus sonatype/nexus3
   ```

3. Wait for Nexus to start (it may take a few minutes). You can check if it's ready by:
   ```bash
   curl -u $NEXUS_USERNAME:$NEXUS_PASSWORD $NEXUS_URL/service/rest/v1/status
   ```

4. Create a PyPI hosted repository in Nexus using curl:
   ```bash
   curl -X POST \
     -u $NEXUS_USERNAME:$NEXUS_PASSWORD \
     -H "Content-Type: application/json" \
     -d '{
       "name": "pypi-hosted",
       "type": "hosted",
       "format": "pypi",
       "online": true,
       "storage": {
         "blobStoreName": "default",
         "strictContentTypeValidation": true,
         "writePolicy": "allow_once"
       }
     }' \
     $NEXUS_URL/service/rest/v1/repositories/pypi/hosted
   ```

5. Verify the repository was created:
   ```bash
   curl -u $NEXUS_USERNAME:$NEXUS_PASSWORD $NEXUS_URL/service/rest/v1/repositories
   ```

6. Configure your local environment:
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

## Error Handling

The calculator library includes error handling for:
- Division by zero
- Invalid input types

The consumer application demonstrates how to handle these errors gracefully.

## Cleanup

To stop and remove the Nexus container:
```bash
docker stop nexus
docker rm nexus
``` 