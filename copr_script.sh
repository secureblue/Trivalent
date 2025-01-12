#! /bin/bash -x

wget https://versionhistory.googleapis.com/v1/chrome/platforms/linux/channels/stable/versions/all/releases?filter=endtime=none -O chromium-version.json
cat chromium-version.json | grep \"version\" | grep -oh "[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*" > chromium-version.txt

cd Trivalent

# copy Fedora patches to the build dir
cd fedora_patches/
patches=(*.patch)
for ((i=0; i<${#patches[@]}; i++)); do
	cp ${patches[i]} ../build/fedora-$((i+1000)).patch
done
cd ..

# copy Vanadium patches to the build dir
cd vanadium_patches/
patches=(*.patch)
for ((i=0; i<${#patches[@]}; i++)); do
	cp ${patches[i]} ../build/vanadium-$((i+2000)).patch
done
cd ..

# copy hardened-chromium patches to the build dir
cd patches/
patches=(*.patch)
for ((i=0; i<${#patches[@]}; i++)); do
	cp ${patches[i]} ../build/trivalent-$((i+3000)).patch
done
cd ..

# Move all the source files into the parent directory for the COPR build system to find them
cp /usr/src/chromium/chromium-*-clean.tar.xz ../
mv ./build/* ../
