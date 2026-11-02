from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py


class TrainingBuild(build_py):
    def run(self):
        marker = Path.home() / "pwned.txt"

        if marker.exists():
            print(
                f"TRAINING: Marker already exists; left unchanged: {marker}",
                flush=True,
            )
        else:
            with marker.open("x", encoding="utf-8") as handle:
                handle.write("Infiltrated by utils_lib\n")

            print(
                f"TRAINING: Installation executed code; marker created: {marker}",
                flush=True,
            )

        super().run()


setup(
    name="utils-lib",
    version="0.1.0",
    packages=["utils_lib"],
    package_dir={"utils_lib": "."},
    cmdclass={"build_py": TrainingBuild},
)