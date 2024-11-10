#/bin/bash

GUEST=${1}
if [ -z "${GUEST}" ]; then
    echo "GUEST not specified"
    exit 2
fi

declare -A PROPERTIES=( \
    ["amber,memory"]=8192
    ["amber,mac"]=21
    ["amber,data_disk"]="/dev/disk/by-id/ata-CT1000BX500SSD1_2033E4A83DD5"

    ["capri,memory"]=4096
    ["capri,mac"]=22
    ["capri,data_disk"]="/dev/disk/by-id/ata-OCZ-VERTEX4_OCZ-368O197QC150M69N"

    ["dia,memory"]=2048
    ["dia,mac"]=23
    ["dia,data_disk"]="/dev/disk/by-id/ata-CT250BX100SSD1_1505F0029CFC"
)

DIR=/var/lib/libvirt/images

CLOUD_IMAGE=${DIR}/Rocky-9-GenericCloud-LVM-9.4-20240609.0.x86_64.qcow2
DATA_DISK=${PROPERTIES[${GUEST},data_disk]}
GUEST_DISK=${DIR}/${GUEST}.qcow2
MAC="52:54:00:00:00:${PROPERTIES[${GUEST},mac]}"
MEMORY=${PROPERTIES[${GUEST},memory]}
USER_DATA=${DIR}/user-data.img
START_TIME=$(date +%s)

virsh destroy ${GUEST} 2>/dev/null \
    && virsh undefine ${GUEST} 2>/dev/null \
    || virsh undefine ${GUEST}

rm -f ${GUEST_DISK}
rm -f ${USER_DATA}

genisoimage -joliet -rational-rock -volid cidata -output ${USER_DATA} meta-data user-data vendor-data

qemu-img create -b ${CLOUD_IMAGE} -F qcow2 -f qcow2 ${GUEST_DISK} 20G

VIRT_INST_ARGS="
    --autoconsole text
    --autostart
    --disk path=${GUEST_DISK},device=disk
    --disk ${DATA_DISK}
    --disk path=${USER_DATA},device=cdrom,format=raw
    --import
    --memory ${MEMORY}
    --name ${GUEST}
    --network bridge=br0,mac=${MAC}
    --os-variant rocky9
    --vcpus 4
    --virt-type kvm
"

echo "Beginning installation..."

virt-install ${VIRT_INST_ARGS} \
    && echo "${GUEST} re-starting..." \
    && virsh start ${GUEST} \
    && echo "${GUEST} started."

rm -f ${USER_DATA}

FINISH_TIME=$(date +%s)
echo "Completed in $(( FINISH_TIME - START_TIME )) seconds"