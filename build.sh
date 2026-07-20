#!/bin/bash
set -e
export PATH="/tmp/clang/bin:${PATH}"
export KBUILD_BUILD_USER="Sukuna567"
export KBUILD_BUILD_HOST="KaliLinux"
export ARCH=arm64
export SUBARCH=arm64
export DEFCONFIG=nemo_defconfig

echo "Generating defconfig..."
mkdir -p out
make O=out ARCH=${ARCH} ${DEFCONFIG}

echo "Starting build..."
make -j$(nproc --all) O=out \
    ARCH=${ARCH} \
    CC="ccache clang" \
    LLVM=1 \
    LLVM_IAS=1 \
    CROSS_COMPILE=aarch64-linux-gnu- \
    CROSS_COMPILE_ARM32=arm-linux-gnueabi- \
    CONFIG_NO_ERROR_ON_MISMATCH=y 2>&1 | tee build.log

if [ ! -f "out/arch/arm64/boot/Image.gz" ]; then
    echo "Image.gz not found! Build failed."
    exit 1
fi

echo "Build successful! Image.gz generated."
