const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  exitApp: () => {
    try {
      ipcRenderer.send('exit-app');
    } catch (e) {}
  }
});
