from setuptools import setup

setup(
    name="app",
    packages=["app"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask",
        "flask_pymongo",
        "flask_api",
        "flask_jwt_extended",
        "flask_bcrypt",
        "marshmallow",
        "flask_testing",
        "requests"
    ],
)
