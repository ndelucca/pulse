#!/usr/bin/bash

pyinstaller --distpath ./dist --workpath ./build --hidden-import=desktop_notifier.resources --onefile --name pulse pulse/cli.py
