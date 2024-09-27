#/bin/bash

GUEST=${1}
if [ -z "${GUEST}" ]; then
    echo "GUEST not specified"
    exit 2
fi

declare -A PROPERTIES=( \
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

cloud-localds ${USER_DATA} user-data

qemu-img create -b ${CLOUD_IMAGE} -F qcow2 -f qcow2 ${GUEST_DISK} 10G

VIRT_INST_ARGS="
    --autostart
    --boot hd,menu=on
    --disk path=${GUEST_DISK},device=disk
    --disk path=${USER_DATA},format=raw
    --disk ${DATA_DISK}
    --graphics none
    --memory ${MEMORY}
    --name ${GUEST}
    --network bridge=br0,mac=${MAC}
    --noautoconsole
    --os-type Linux
    --os-variant rhel8-unknown
    --vcpus 4
    --virt-type kvm
"

echo "Beginning installation..."

virt-install ${VIRT_INST_ARGS} \
    && echo "${GUEST} installation started. Connecting to console..." \
    && virsh console ${GUEST} \
    && echo "${GUEST} installation complete. Removing cloud-init user-data disk..." \
    && virsh detach-disk ${GUEST} ${USER_DATA} --persistent \
    && echo "${GUEST} re-starting..." \
    && virsh start ${GUEST} \
    && echo "${GUEST} started."

rm -f ${USER_DATA}

FINISH_TIME=$(date +%s)
echo "Completed in $(( FINISH_TIME - START_TIME )) seconds"
