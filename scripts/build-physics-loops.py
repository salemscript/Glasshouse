"""Compatibility entry point; the full manifest builder owns question matching."""
import pathlib,runpy
runpy.run_path(str(pathlib.Path(__file__).with_name('build-physics-illustrations.py')),run_name='__main__')
