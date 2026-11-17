const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('studioApp', {
  begin: (o) => ipcRenderer.invoke('exp:begin', o),
  frame: (buf) => ipcRenderer.invoke('exp:frame', buf),
  finish: (o) => ipcRenderer.invoke('exp:finish', o),
  cancel: () => ipcRenderer.invoke('exp:cancel'),
});
