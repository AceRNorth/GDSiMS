#!/bin/sh
# Code adapted from Martin Fitzpatrick, "Packaging PyQt5 applications into a macOS app with PyInstaller", Python GUIs
# https://www.pythonguis.com (March 10 2025) under a BSD & MIT copyright licence.

# Copyright 2014-2025 Martin Fitzpatrick

# BSD:
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in
# the documentation and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE 
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# MIT:
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the
# “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, 
# publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Before running this script, run "brew install create-dmg"

mkdir -p dist_mac/dmg
rm -r dist_mac/dmg/*
cp -r "dist_mac/GDSiMS.app" dist_mac/dmg
test -f "dist_mac/GDSiMS.dmg" && rm "dist_mac/GDSiMS.dmg"
create-dmg \
	--volname "GDSiMS" \
	--window-pos 200 120 \
	--window-size 600 300 \
	--icon-size 100 \
	--icon "GDSiMS.app" 175 120 \
	--hide-extension "GDSiMS.app" \
	--app-drop-link 425 120 \
	"dist_mac/GDSiMS.dmg" \
	"dist_mac/dmg/"

