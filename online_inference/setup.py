from setuptools import find_packages, setup


with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name="heart_disease_online_inference",
    packages=find_packages(),
    version="0.1.0",
    description="Example of ml project - heart_disease_online_inference",
    author="spin to win",
    install_requires=required,
    license="MIT",
)
