# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.26
# 

Name:       u-boot-sunxi

# >> macros
# << macros

Summary:    The u-boot firmware for sunxi boards
Version:    2013.01
Release:    1
Group:      System/Boot
License:    GPL
ExclusiveArch:  %{arm}
URL:        http://linux-sunxi.org/Main_Page
Source0:    %{name}-%{version}.tar.bz2
Source1:    u-boot-sunxi.cmd
Source2:    u-boot-sunxi-spec-file-helper.sh
Source3:    README-PACKAGER.txt
Source100:  u-boot-sunxi.yaml
Patch0:     0001-no-fel.diff
Requires:   u-boot-sunxi-eoma68_a20
Requires:   u-boot-sunxi-doc
Requires:   u-boot-sunxi-tools
Provides:   u-boot

%description
Das U-Boot (or just "U-Boot" for short) is Open Source Firmware for Embedded PowerPC, ARM, MIPS and x86 processors.


%package doc
Summary:    Documentation for the u-boot Firmware
Group:      Documentation

%description doc
Das U-Boot (or just "U-Boot" for short) is Open Source Firmware for Embedded PowerPC, ARM, MIPS and x86 processors.
This package contains documentation for u-boot firmware


%package tools
Summary:    Tools for the u-boot Firmware
Group:      System/Boot

%description tools
Das U-Boot (or just "U-Boot" for short) is Open Source Firmware for Embedded PowerPC, ARM, MIPS and x86 processors.
This package contains:
mkimage- a tool that creates kernel bootable images for u-boot.


%package eoma68_a20
Summary:    U-boot files of board eoma68_a20
Group:      System/Boot

%description eoma68_a20
This package contain board specifiy u-boot files


%prep
%setup -q -n %{name}-%{version}/u-boot-sunxi

# 0001-no-fel.patch
%patch0 -p1
# >> setup
# << setup

%build
# >> build pre
# << build pre



# >> build post


TMP_DIR=../boot/

make EOMA68_A20_FEL

mkdir -p ${TMP_DIR}
cp %{SOURCE1} ${TMP_DIR}/u-boot.cmd
install -D -m 0644 u-boot.bin ${TMP_DIR}/u-boot.bin
install -D -m 0644 u-boot.map ${TMP_DIR}/u-boot.map
./tools/mkimage -A arm -O linux -T script -C none -a 0 -e 0 \
-n "Sunxi  SD Boot" \
-d ${TMP_DIR}/u-boot.cmd ${TMP_DIR}/boot.scr

if [ -n "$(ls spl/* | grep 'spl.bin')" ]; then
cp spl/u-boot-spl.bin ${TMP_DIR}/u-boot-spl.bin
#cp spl/sunxi-spl.bin ${TMP_DIR}/sunxi-spl.bin
cp spl/u-boot-spl.lds ${TMP_DIR}/u-boot-spl.lds
cp spl/u-boot-spl.map ${TMP_DIR}/u-boot-spl.map
fi

# << build post

%install
rm -rf %{buildroot}
# >> install pre
# << install pre

# >> install post
mkdir -p %{buildroot}
mv ../boot %{buildroot}/boot
install -D -m 0755 tools/mkimage %{buildroot}%{_bindir}/mkimage
install -D -m 0644 doc/mkimage.1 %{buildroot}%{_mandir}/man1/mkimage.1
gzip %{buildroot}%{_mandir}/man1/*

find %{buildroot} | sort
# << install post

%files
%defattr(-,root,root,-)
%doc CREDITS
# >> files
# << files

%files doc
%defattr(-,root,root,-)
%doc README doc/README.JFFS2 doc/README.JFFS2_NAND doc/README.commands
%doc doc/README.autoboot doc/README.commands doc/README.console doc/README.dns
%doc doc/README.hwconfig doc/README.nand doc/README.NetConsole doc/README.serial_multi
%doc doc/README.SNTP doc/README.standalone doc/README.update doc/README.usb
%doc doc/README.video doc/README.VLAN doc/README.silent doc/README.POST doc/README.Modem
%doc tools/scripts/dot.kermrc tools/scripts/flash_param tools/scripts/send_cmd tools/scripts/send_image
%doc doc/README.ARM-SoC doc/README.ARM-memory-map
# >> files doc
# << files doc

%files tools
%defattr(-,root,root,-)
%{_bindir}/mkimage
%{_mandir}/man1/mkimage.1.gz
# >> files tools
# << files tools

%files eoma68_a20
%defattr(-,root,root,-)
/boot/*
# >> files eoma68_a20
# << files eoma68_a20
