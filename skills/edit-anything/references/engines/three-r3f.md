# three.js, React Three Fiber, Rapier and postprocessing

**What it is.** three.js (MIT) draws 3D in the browser. React Three Fiber writes it as React components; `@react-three/rapier` adds physics (falling, colliding, stacking); `@react-three/postprocessing` adds an effects chain (bloom, depth of field, grain, vignette, chromatic aberration). All MIT (pmndrs).

**The method for film.** Build the scene as a function of time: set the camera, objects and the physics state from `t`, not from a running clock. For physics, simulate once at a fixed step, record the positions per frame, and play the recording back by `t`, so every render is identical. Render frame by frame in headless Chrome and pipe to ffmpeg.

**Use it for.** Product turntables, abstract 3D explainers, a previs of a camera move before a generated shot (Tein's Previs workflow uses a three.js blockout as the camera reference for Seedance).

**Where it fails.** Organic characters and realistic materials (Blender or generated shots), long scenes on weak GPUs.
