// Explainer Studio, desktop shell: shows the studio page and turns frames from the page into an MP4 with the bundled ffmpeg.
const { app, BrowserWindow, ipcMain, dialog, shell } = require('electron');
const { spawn, spawnSync } = require('node:child_process');
const fs = require('node:fs'), path = require('node:path'), os = require('node:os');
let ffmpeg = require('ffmpeg-static'); if (ffmpeg.includes('app.asar')) ffmpeg = ffmpeg.replace('app.asar', 'app.asar.unpacked');
let win = null, S = null;
const SELFTEST = process.argv.includes('--selftest');

function createWindow() {
  win = new BrowserWindow({ width: 1560, height: 980, minWidth: 900, minHeight: 640, backgroundColor: '#14100d', title: 'Explainer Studio', webPreferences: { preload: path.join(__dirname, 'preload.js'), contextIsolation: true, backgroundThrottling: false, nodeIntegration: false, autoplayPolicy: 'no-user-gesture-required' } });
  if (SELFTEST) win.webContents.on('console-message', (e, level, msg) => console.log('PAGE', level, String(msg).slice(0, 200)));
  win.loadFile(path.join(__dirname, 'studio.html'));
  win.webContents.setWindowOpenHandler(({ url }) => { shell.openExternal(url); return { action: 'deny' }; });
  if (SELFTEST) win.webContents.on('did-finish-load', async () => {
    try { await new Promise((r) => setTimeout(r, 4000)); const out = path.join(os.tmpdir(), 'studio-selftest.mp4'); const r = await win.webContents.executeJavaScript(`window.__selftest(${JSON.stringify(out)})`); console.log('SELFTEST', JSON.stringify(r), fs.existsSync(out) ? fs.statSync(out).size : 'no file'); } catch (e) { console.log('SELFTEST ERROR', e && e.message); } app.quit();
  });
}
app.whenReady().then(createWindow); app.on('window-all-closed', () => app.quit());

ipcMain.handle('exp:begin', async (e, o) => {
  let out = o.out;
  if (!out) { const r = await dialog.showSaveDialog(win, { title: 'Save the film', defaultPath: path.join(app.getPath('downloads'), o.name || 'film.mp4'), filters: [{ name: 'MP4 video', extensions: ['mp4'] }] }); if (r.canceled || !r.filePath) return null; out = r.filePath; }
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'studio-')), video = path.join(tmp, 'video.mp4');
  const ff = spawn(ffmpeg, ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(o.fps), '-c:v', 'png', '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '14', '-r', String(o.fps), video], { stdio: ['pipe', 'ignore', 'pipe'] });
  let err = ''; ff.stderr.on('data', (d) => { err += d; }); S = { ff, tmp, video, out, fps: o.fps, errs: () => err, closed: new Promise((r) => ff.on('close', r)) };
  return out;
});
ipcMain.handle('exp:frame', (e, buf) => new Promise((res) => { if (!S) return res(false); S.ff.stdin.write(Buffer.from(buf), () => res(true)); }));
ipcMain.handle('exp:cancel', () => { if (S) { try { S.ff.kill(); } catch (e2) {} S = null; } return true; });
ipcMain.handle('exp:finish', async (e, o) => {
  if (!S) return { error: 'No export running.' }; const s = S; S = null; s.ff.stdin.end(); await s.closed;
  const fx = path.join(s.tmp, 'fx.f32'), fxw = path.join(s.tmp, 'fx.wav'); fs.writeFileSync(fx, Buffer.from(o.effects)); spawnSync(ffmpeg, ['-y', '-v', 'error', '-f', 'f32le', '-ar', '48000', '-ac', '2', '-i', fx, fxw]);
  let args; const S2 = o.seconds, prep = `apad=whole_dur=${S2},atrim=0:${S2}`, outro = `loudnorm=I=-16:TP=-1.5:LRA=11,aformat=sample_rates=48000:channel_layouts=stereo[a]`;
  const inputs = ['-i', s.video]; let n = 1, vI = -1, fI, mI = -1;
  if (o.voice) { const vf = path.join(s.tmp, 'voice.bin'); fs.writeFileSync(vf, Buffer.from(o.voice)); inputs.push('-i', vf); vI = n++; }
  inputs.push('-i', fxw); fI = n++;
  if (o.music) { const mf = path.join(s.tmp, 'music.bin'); fs.writeFileSync(mf, Buffer.from(o.music)); const mh = path.join(s.tmp, 'music_h.wav'); spawnSync(ffmpeg, ['-y', '-v', 'error', '-i', mf, '-filter_complex', '[0:a]asplit[a][b];[b]highpass=f=60,volume=30,asoftclip=type=tanh,highpass=f=150,lowpass=f=2500,volume=0.35[h];[a][h]amix=inputs=2:normalize=0,alimiter=limit=0.9', mh]); inputs.push('-i', mh); mI = n++; }
  const f = [];
  if (vI > 0 && mI > 0) { f.push(`[${vI}:a]${prep},loudnorm=I=-17:TP=-2,asplit=3[v1][v2][v3]`, `[${fI}:a]${prep},loudnorm=I=-26:TP=-4:LRA=20[fx0]`, `[fx0][v1]sidechaincompress=threshold=0.05:ratio=3:attack=10:release=250[fx]`, `[${mI}:a]${prep},afade=t=in:st=0:d=1.5,afade=t=out:st=${Math.max(0, S2 - 3.5)}:d=3.5,loudnorm=I=-16:TP=-3:LRA=20,volume=${0.4}[mu0]`, `[mu0][v3]sidechaincompress=threshold=0.08:ratio=2:attack=30:release=600[mu]`, `[v2][fx][mu]amix=inputs=3:normalize=0,${outro}`); }
  else if (vI > 0) { f.push(`[${vI}:a]${prep},loudnorm=I=-17:TP=-2,asplit=2[v1][v2]`, `[${fI}:a]${prep},loudnorm=I=-26:TP=-4:LRA=20[fx0]`, `[fx0][v1]sidechaincompress=threshold=0.05:ratio=3:attack=10:release=250[fx]`, `[v2][fx]amix=inputs=2:normalize=0,${outro}`); }
  else if (mI > 0) { f.push(`[${fI}:a]${prep},loudnorm=I=-26:TP=-4:LRA=20[fx0]`, `[${mI}:a]${prep},afade=t=in:st=0:d=1.5,afade=t=out:st=${Math.max(0, S2 - 3.5)}:d=3.5,loudnorm=I=-20:TP=-3:LRA=20[mu0]`, `[fx0][mu0]amix=inputs=2:normalize=0,${outro}`); }
  else f.push(`[${fI}:a]${prep},loudnorm=I=-18:TP=-2,aformat=sample_rates=48000:channel_layouts=stereo[a]`);
  args = ['-y', '-v', 'error', ...inputs, '-filter_complex', f.join(';'), '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-ar', '48000', '-ac', '2', '-b:a', '192k', '-t', String(S2), '-movflags', '+faststart', s.out];
  const r = spawnSync(ffmpeg, args); try { fs.rmSync(s.tmp, { recursive: true, force: true }); } catch (e3) {}
  if (r.status !== 0) return { error: 'ffmpeg failed: ' + String(r.stderr).slice(0, 300) };
  if (!SELFTEST) shell.showItemInFolder(s.out); return { out: s.out, bytes: fs.statSync(s.out).size };
});
