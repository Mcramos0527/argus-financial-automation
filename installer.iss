; ARGUS — Script de Inno Setup para generar el instalador Windows
; Powered by McFlow
;
; Prerrequisitos:
;   1. pip install pyinstaller
;   2. pyinstaller --onefile --windowed --name ARGUS --icon icon.ico main.py
;   3. Abrir este .iss con Inno Setup Compiler y compilar

[Setup]
AppName=ARGUS
AppVersion=1.0.0
AppPublisher=McFlow
AppPublisherURL=https://mcflow.com
AppSupportURL=https://mcflow.com/soporte
AppUpdatesURL=https://mcflow.com/actualizaciones
DefaultDirName={autopf}\ARGUS
DefaultGroupName=ARGUS
AllowNoIcons=yes
OutputDir=installer_output
OutputBaseFilename=ARGUS_Setup_v1.0.0
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el Escritorio"; GroupDescription: "Íconos adicionales:"
Name: "quicklaunchicon"; Description: "Crear acceso directo en la Barra de inicio rápido"; GroupDescription: "Íconos adicionales:"; Flags: unchecked

[Files]
; El ejecutable generado por PyInstaller
Source: "dist\ARGUS.exe"; DestDir: "{app}"; Flags: ignoreversion

; Si PyInstaller genera una carpeta en lugar de un solo .exe, usar esto:
; Source: "dist\ARGUS\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\ARGUS"; Filename: "{app}\ARGUS.exe"
Name: "{group}\{cm:UninstallProgram,ARGUS}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\ARGUS"; Filename: "{app}\ARGUS.exe"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\ARGUS"; Filename: "{app}\ARGUS.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\ARGUS.exe"; Description: "{cm:LaunchProgram,ARGUS}"; Flags: nowait postinstall skipifsilent
