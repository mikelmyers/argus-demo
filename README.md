# argus-diff demo

A tiny repo that exists to show [argus-diff](https://argusdiff.com) working
on pull requests. `cad/bracket.step` is a sensor-mount bracket; open a PR
that changes it and the Argus action comments the geometric diff — bodies
added/removed/modified, mass delta, face-level changes, interference — with
renders attached as artifacts.

Try it: fork, regenerate the bracket with different parameters
(`python make_bracket.py --thickness 8 --hole 6`), open a PR.

The live demo PR in this repo changes the plate thickness 6→8 mm, opens the
corner holes ⌀5→⌀6, grows the boss, adds a gusset, and deletes a locating
pin. The action catches all of it, including a deliberate 109 mm³
gusset/boss interference.
