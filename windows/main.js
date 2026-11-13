const { app, BrowserWindow, Menu } = require('electron');
const path = require('path');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 768,
    minWidth: 960,
    minHeight: 540,
    title: "RC Car in Class - 3D Classroom Racing",
    icon: path.join(__dirname, 'icon-192.png'),
    backgroundColor: '#0a0a14',
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      webSecurity: false, // Allows loading local glb 3D assets and audio via file:// protocol
      allowRunningInsecureContent: true
    },
    autoHideMenuBar: true
  });

  // Load the web game entry point
  mainWindow.loadFile('index.html');

  // Handle window closed
  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // Shortcuts: F11 for Fullscreen, F12 for DevTools (optional), F5 for Reload
  mainWindow.webContents.on('before-input-event', (event, input) => {
    if (input.key === 'F11' && input.type === 'keyDown') {
      mainWindow.setFullScreen(!mainWindow.isFullScreen());
      event.preventDefault();
    } else if (input.key === 'Escape' && input.type === 'keyDown' && mainWindow.isFullScreen()) {
      mainWindow.setFullScreen(false);
      event.preventDefault();
    } else if (input.key === 'F5' && input.type === 'keyDown') {
      mainWindow.reload();
      event.preventDefault();
    }
  });
}

// App lifecycle
app.whenReady().then(() => {
  Menu.setApplicationMenu(null);
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
