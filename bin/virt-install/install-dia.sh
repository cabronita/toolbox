#/bin/bash

GUEST=dia
MAC=52:54:00:00:00:23

DIR=/var/lib/libvirt/images
START_TIME=$(date +%s)

virsh destroy ${GUEST} 2>/dev/null \
    && virsh undefine ${GUEST} 2>/dev/null \
    || virsh undefine ${GUEST}

rm -f ${DIS}/${GUEST}-disk.qcow2
rm -f ${DIR}user-data.img

cloud-localds ${DIR}/user-data.img user-data

qemu-img create \
    -b ${DIR}/Rocky-9-GenericCloud-LVM-9.4-20240609.0.x86_64.qcow2 \
    -F qcow2 \
    -f qcow2 ${DIR}/${GUEST}-disk.qcow2 10G

VIRT_INST_ARGS="
    --autostart
    --boot hd,menu=on
    --disk path=${DIR}/${GUEST}-disk.qcow2,device=disk
    --disk path=${DIR}/user-data.img,format=raw
    --disk /dev/disk/by-id/ata-CT250BX100SSD1_1505F0029CFC
    --graphics none
    --memory 4096
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
    && virsh detach-disk dia /var/lib/libvirt/images/user-data.img --persistent \
    && echo "${GUEST} re-starting..." \
    && virsh start ${GUEST} \
    && echo "${GUEST} started."

rm -f ${DIR}/user-data.img

FINISH_TIME=$(date +%s)
echo "Completed in $(( FINISH_TIME - START_TIME )) seconds"
