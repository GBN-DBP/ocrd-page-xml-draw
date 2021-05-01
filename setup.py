import setuptools

with open("requirements.txt", 'r') as fp:
    install_requires = fp.read()

with open("README.md", 'r') as fp:
    long_description = fp.read()

setuptools.setup(
    name="ocrd-page-xml-draw",
    version="0.0.1",
    author="Lucas Sulzbach",
    author_email="lucas@sulzbach.org",
    description="OCR-D wrapper for page-xml-draw",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GBN-DBP/ocrd-page-xml-draw",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    package_data={
      "": ["*.json"]
    },
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Utilities",
    ],
    entry_points={
      "console_scripts": [
        "ocrd-page-xml-draw=ocrd_page_xml_draw:ocrd_page_xml_draw",
      ]
    },
    python_requires='>=3.6',
)
