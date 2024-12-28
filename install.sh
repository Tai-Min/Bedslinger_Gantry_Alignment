HOME_DIR="${HOME}/klipper"

if [  -d "$1" ] ; then

	echo "$1"
	HOME_DIR=""$1"/klipper"
fi

REPODIR="$( cd "$( dirname "$0" )" && pwd )"

if [ ! -d "$HOME_DIR" ] ; then
    echo ""
    echo "path error doesn't exist in "$HOME_DIR""
    echo ""
    echo "Plugin path: "$REPODIR""
    echo ""
    echo "usage:./install.sh /home/pi"
    exit 1
fi

echo "Linking ${REPODIR}/bedslinger_gantry_alignment.py to klippy..."

if [ -e "${HOME_DIR}/klippy/extras/bedsligner_gantry_alignment.py" ]; then
    rm "${HOME_DIR}/klippy/extras/bedsligner_gantry_alignment.py"
fi
ln -s "${REPODIR}/bedsligner_gantry_alignment.py" "${HOME_DIR}/klippy/extras/bedsligner_gantry_alignment.py"

echo "Done"
