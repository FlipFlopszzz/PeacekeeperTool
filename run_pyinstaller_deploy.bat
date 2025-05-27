pyinstaller -D -n PeacekeeperTool --windowed --add-data "translations/*.qm:translations" --add-data "resources/warmup.wav:assets" src/main.py
cd .\dist\PeacekeeperTool\_internal\PySide6 
rmdir /s /q translations 
del /q opengl32sw.dll Qt6Network.dll Qt6OpenGL.dll Qt6Pdf.dll Qt6Qml.dll Qt6QmlMeta.dll Qt6QmlModels.dll Qt6QmlWorkerScript.dll Qt6Quick.dll Qt6Svg.dll Qt6VirtualKeyboard.dll
cd plugins
rmdir /s /q generic styles tls iconengines imageformats networkinformation platforminputcontexts