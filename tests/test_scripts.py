"""Tests for the scripts that ship with this skill. Run: python -m unittest discover -s tests -v"""
import csv
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = "edit-anything"


def path(*parts):
    return os.path.join(ROOT, "skills", SKILL, *parts)


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, file)
    mod = importlib.util.module_from_spec(spec)
    sys.argv = [file]
    spec.loader.exec_module(mod)
    return mod


def run(*args, stdin=None):
    return subprocess.run([sys.executable, *args], capture_output=True, text=True, input=stdin)


HAVE_FFMPEG = subprocess.run(["which", "ffmpeg"], capture_output=True).returncode == 0


def make_video(folder, seconds=2, size="1080x1920", volume="-14dB", black=False, audio=True):
    out = os.path.join(folder, "clip.mp4")
    color = "black" if black else "0x388E3C"
    args = ["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", f"color=c={color}:s={size}:d={seconds}:r=30"]
    if audio:
        args += ["-f", "lavfi", "-i", f"sine=f=440:d={seconds}", "-af", f"volume={volume}", "-c:a", "aac"]
    args += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-shortest", out]
    subprocess.run(args, check=True)
    return out


class CheckDossier(unittest.TestCase):
    script = path("scripts", "check_dossier.py")
    template = path("templates", "edit.json")

    def gate(self, data, gate):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(data, f)
        return run(self.script, f.name, "--gate", gate)

    def test_template_passes_every_gate(self):
        data = json.load(open(self.template))
        for g in ("1", "2", "deliver"):
            self.assertEqual(self.gate(data, g).returncode, 0, g)

    def test_gate1_needs_all_mood_axes(self):
        data = json.load(open(self.template))
        data["mood"].pop("pace", None)
        self.assertNotEqual(self.gate(data, "1").returncode, 0)

    def test_gate2_needs_quote_for_generated_rows(self):
        data = json.load(open(self.template))
        rows = data["board"]
        rows[0]["shot_type"] = "generated"
        rows[0]["quote_approved"] = False
        self.assertNotEqual(self.gate(data, "2").returncode, 0)

    def test_deliver_needs_passed_verify(self):
        data = json.load(open(self.template))
        data["verify"]["passed"] = False
        self.assertNotEqual(self.gate(data, "deliver").returncode, 0)


@unittest.skipUnless(HAVE_FFMPEG, "ffmpeg not installed")
class Beats(unittest.TestCase):
    def test_fixed_bpm_grid(self):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "beats.json")
            wav = os.path.join(d, "x.wav")
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "sine=f=220:d=4", wav], check=True)
            r = run(path("scripts", "beats.py"), wav, "--bpm", "120", "--out", out)
            self.assertEqual(r.returncode, 0, r.stderr)
            data = json.load(open(out))
            beats = data["beats"]
            self.assertAlmostEqual(beats[1] - beats[0], 0.5, places=3)


class Handoff(unittest.TestCase):
    def edl(self, folder):
        data = {"fps": 30, "width": 1080, "height": 1920,
                "clips": [{"file": "a.mp4", "in": 0.0, "out": 1.5}, {"file": "b.mp4", "in": 2.0, "out": 3.0}],
                "audio": [{"file": "voice.wav", "start": 0.0, "in": 0.0, "out": 2.5, "role": "voice"}],
                "captions": [{"start": 0.0, "end": 1.2, "text": "Hello there"}, {"start": 1.2, "end": 2.5, "text": "Two"}]}
        p = os.path.join(folder, "edit.json")
        json.dump(data, open(p, "w"))
        return p

    def test_fcpxml_edl_srt_and_kit(self):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "out")
            r = run(path("scripts", "handoff.py"), self.edl(d), "--out", out, "--fcpxml", "--edl", "--srt", "--mobile-kit")
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            names = os.listdir(out)
            fcp = [n for n in names if n.endswith(".fcpxml")]
            self.assertTrue(fcp)
            import xml.dom.minidom
            xml.dom.minidom.parse(os.path.join(out, fcp[0]))
            self.assertTrue(any(n.endswith(".edl") for n in names))
            srt = open(os.path.join(out, [n for n in names if n.endswith(".srt")][0])).read()
            self.assertIn("00:00:01,200", srt)

    def test_bad_clip_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = self.edl(d)
            data = json.load(open(p))
            data["clips"][0]["out"] = 0.0
            json.dump(data, open(p, "w"))
            r = run(path("scripts", "handoff.py"), p, "--out", os.path.join(d, "o"), "--edl")
            self.assertNotEqual(r.returncode, 0)


@unittest.skipUnless(HAVE_FFMPEG, "ffmpeg not installed")
class VerifyExport(unittest.TestCase):
    script = path("scripts", "verify_export.py")

    def test_quiet_audio_fails(self):
        with tempfile.TemporaryDirectory() as d:
            r = run(self.script, make_video(d, volume="-40dB"), "--target", "social", "--shape", "9:16")
            self.assertEqual(r.returncode, 1)

    def test_black_frames_fail(self):
        with tempfile.TemporaryDirectory() as d:
            r = run(self.script, make_video(d, black=True), "--max-black", "0.5")
            self.assertEqual(r.returncode, 1)

    def test_wrong_shape_fails(self):
        with tempfile.TemporaryDirectory() as d:
            r = run(self.script, make_video(d, size="1920x1080"), "--shape", "9:16")
            self.assertEqual(r.returncode, 1)

    def test_audio_cut_short_fails(self):
        with tempfile.TemporaryDirectory() as d:
            v = make_video(d, seconds=3)
            out = os.path.join(d, "short.mp4")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", v, "-af", "atrim=0:1.5", "-c:v", "copy", out], check=True)
            r = run(self.script, out)
            self.assertEqual(r.returncode, 1)
            self.assertIn("cut off", r.stdout)

    def test_missing_audio_fails(self):
        with tempfile.TemporaryDirectory() as d:
            r = run(self.script, make_video(d, audio=False))
            self.assertEqual(r.returncode, 1)


class HarnessCheck(unittest.TestCase):
    def test_runs_and_never_prints_keys(self):
        env = dict(os.environ, ELEVENLABS_API_KEY="sk-secret-123")
        r = subprocess.run([sys.executable, path("scripts", "harness_check.py")], capture_output=True, text=True, env=env)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("sk-secret-123", r.stdout)
        self.assertIn("ELEVENLABS_API_KEY", r.stdout)


class Hook(unittest.TestCase):
    hook = os.path.join(ROOT, "hooks", "check_reply.py")

    def reply(self, text, tool=None, skill=SKILL, active=False):
        entries = [{"type": "user", "message": {"content": "please use " + SKILL}}]
        if tool:
            entries.append({"type": "assistant", "message": {"content": [{"type": "tool_use", "name": tool, "input": {}}]}})
        entries.append({"type": "assistant", "message": {"content": [{"type": "text", "text": text}]}})
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as f:
            f.write("\n".join(json.dumps(e) for e in entries))
        r = run(self.hook, skill, stdin=json.dumps({"transcript_path": f.name, "stop_hook_active": active}))
        return r.stdout.strip()

    def test_one_question_passes(self):
        self.assertEqual(self.reply("What should the viewer feel at the end?"), "")

    def test_two_questions_block(self):
        self.assertIn("block", self.reply("How many per week? And who makes them?"))

    def test_compound_question_blocks(self):
        self.assertIn("block", self.reply("How many per week, and who makes them?"))

    def test_gap_list_counts_as_one(self):
        self.assertEqual(self.reply("Three quick gaps:\n1. Which channel?\n2. Which date?\n3. Price?"), "")

    def test_quoted_question_ignored(self):
        self.assertEqual(self.reply('She asked "is this right?". What does your week look like?'), "")

    def test_to_whom_compound_blocks(self):
        self.assertIn("block", self.reply("What do you sell, and to whom?"))

    def test_translation_line_ignored(self):
        self.assertEqual(self.reply("Wil je erbij zijn?\nIn English: Want to join?"), "")

    def test_note_to_self_blocks(self):
        self.assertIn("block", self.reply("Note to self: run the script. How many?"))

    def test_false_save_claim_blocks(self):
        self.assertIn("block", self.reply("I added this to business-context.md."))
        self.assertEqual(self.reply("I added this to business-context.md.", tool="Write"), "")

    def test_inactive_skill_and_loop_guard(self):
        self.assertEqual(self.reply("A? B?", skill="some-other-skill"), "")
        self.assertEqual(self.reply("A? B?", active=True), "")


if __name__ == "__main__":
    unittest.main()
