# Stop script if a command fails
set -e

# Create python virtual environment and activate it.
python3 -m venv ./venv || echo "failed to make venv"
echo "  Python virtual env created"

# Install python dependencies.
pip install -r reqs.txt || echo "failed to pip install py reqs"
echo "  Python dependencies installed"

# Install javascript dependencies.
cd ./app/static/
npm install || echo "failed to npm install"
cd -
echo "  JS dependencies installed"

echo ""
echo "  Install complete!"