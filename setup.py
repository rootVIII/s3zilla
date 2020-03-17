from setuptools import setup


setup(
    name="s3zilla",
    version="1.0.1",
    packages=["s3zilla"],
    package_data={
        's3zilla': ['s3zilla/*']
    },
    include_package_data=True,
    url="https://github.com/rootVIII/s3zilla",
    license="MIT",
    author="rootVIII",
    description="Simple, Cross-Platform, File-XFER Client for Amazon S3",
    entry_points={
        "console_scripts": [
            "s3zilla=s3zilla.s3_zilla:main"
        ]
    },
    data_files=[
        (
            's3zilla', [
                's3zilla/icon.png',
                's3zilla/icon.ico'
            ]
        )
    ]
)
