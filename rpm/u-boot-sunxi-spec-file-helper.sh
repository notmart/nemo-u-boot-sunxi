#!/bin/bash
set -e
export LANG=C

TEMP_DIR=$(mktemp -d)
TARBALL=$(ls *.tar.* | sort -r | head -n 1)
TARBALL_PREFIX=$(echo ${TARBALL} | sed "s|\.tar\..*||g")
CONFIG_FILE=boards.cfg

PACKAGE=u-boot-sunxi
GROUP="System/Boot"
SUMMARY="U-boot files of board"
DESCRIPTION="This package contain board specifiy u-boot files"
VALID_SUB_PACKAGES="doc|tools|eoma68_a10"

if [ -n "$(echo ${TARBALL} | grep 'xz$')" ];then
    IDENTIFIER=$(echo ${TARBALL} | sed 's|\.xz||g')
    cp ${TARBALL} ${TEMP_DIR}
    xz -d ${TEMP_DIR}/${TARBALL}
    tar -C ${TEMP_DIR} \
        -xvf ${TEMP_DIR}/${IDENTIFIER} \
        ${TARBALL_PREFIX}/${CONFIG_FILE} \
        --strip-components=1 \
        > /dev/null   
else
    tar -C ${TEMP_DIR} \
        -xvf ${TARBALL} \
        ${TARBALL_PREFIX}/${CONFIG_FILE} \
        --strip-components=1 \
        > /dev/null
fi

MAKE_TARGETS=$(grep sunxi ${TEMP_DIR}/${CONFIG_FILE} | awk '{print $1}')
# Add new subpackages if the tarball contain make target
for make_target in ${MAKE_TARGETS}; do
    FILE_PREFIX=${make_target}

    SUB_PACKAGE=$(basename ${make_target} | \
        sed 's|+|plus|g' | \
        sed 's|\.|dot|g')

    # Add new subpackages
    if [ -z "$(egrep "Name:  ${SUB_PACKAGE}$" *.yaml)" ]; then
        specify --newsub=${SUB_PACKAGE}
        sed -i "s|Requires:|Requires:\n    - ${PACKAGE}-${SUB_PACKAGE}|g" *.yaml
        sed -i "s|Summary: ^^^|Summary: ${SUMMARY} ${SUB_PACKAGE}|g" *.yaml
        sed -i "s|Group: ^^^|Group: ${GROUP}|g" *.yaml
        sed -i '/"^^^"/d' *.yaml
        echo "      AutoDepend: false" >> *.yaml
        echo "      Description: |" >> *.yaml
        echo "          ${DESCRIPTION}" >>  *.yaml
        echo "" >>  *.yaml
        echo "      Files:" >> *.yaml
        echo "          - /boot/${FILE_PREFIX}-*" >> *.yaml
    fi
done

# Remove from tarball dropped subpackage
SUB_PACKAGES=$(grep '\- Name:' *.yaml | sed 's|\- Name:||g' | sed 's| ||g' | egrep -v "${VALID_SUB_PACKAGES}")
for subpackage in ${SUB_PACKAGES}; do
    MAYBE_RENAMED=$(echo ${subpackage} | \
        sed 's|plus|+|g' | \
        sed 's|dot|.|g')
    if [ -z "$(echo ${MAKE_TARGETS} | grep "${subpackage}" )" ]; then
       echo "Warning tarball does not contain Makefile target: ${subpackage}"
       if [ -n "$(echo ${BOARD_CONFIGS} | grep "${MAYBE_RENAMED}")" ]; then
           echo -n "Package was most likely renamed by rpm convention from: "
           echo "${MAYBE_RENAMED}"
       else
           echo "Remove from tarball dropped package: ${subpackage}"
           sed -i "/- Name:  ${subpackage}/,+9d" *.yaml
           sed -i "/- ${PACKAGE}-${subpackage}$/d" *.yaml
       fi
    fi
done

# Update spec file
specify
rm -rf ${TEMP_DIR}
