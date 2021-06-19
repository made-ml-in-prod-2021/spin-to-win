from setuptools import find_packages, setup

setup(
    name="heart_disease",
    packages=find_packages(),
    version="0.1.0",
    description="Example of ml project - heart_disease",
    author="spin to win",
    install_requires=[
        "click==7.1.2",
        "python-dotenv>=0.5.1",
        "scikit-learn==0.24.1",
        "dataclasses==0.6",
        "pyyaml==5.4.1",
        "marshmallow-dataclass==8.3.0",
        "pandas==1.1.5",
        "hydra-core==1.0.6",
        "omegaconf==2.0.6",
        "pytest==6.1.2",
        "pytest-cov==2.10.1",
        "tox==3.23.1",
        "Faker==8.1.4",
    ],
    license="MIT",
)
