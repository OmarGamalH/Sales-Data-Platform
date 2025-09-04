echo "WARNING: SET PYTHON_HOME to the path of python directory \n
EX: export PYTHON_HOME=/the/path/to/python \n
Example of PYTHON_HOME is /usr/lib/python3.12/\n"

PROJECT_HOME=$(pwd)
# Making folder for default python search for libraries
echo "Creating the Packages Folder in Root Path...\n"

cd ~
sudo mkdir "packages"

cd "$PROJECT_HOME"
sudo cp ./dags/Utilities ~/packages

cd "$PYTHON_HOME"/dist-packages
echo "~/packages/" > my-path.pth

echo "\nDone.\n"






