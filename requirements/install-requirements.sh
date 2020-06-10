installPackage(){
    MODULE=$1
    DIR="${HOME}/apps/packages/${MODULE}"
    if [ ! -d "$DIR" ]; then
        git clone http://github.com/steel-a/${MODULE} $DIR
        sh ${DIR}/requirements/install-requirements.sh
    else echo "Dir already exists: ${DIR}"
    fi
}

installPackage dbpy
