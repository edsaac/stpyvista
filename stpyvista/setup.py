from pathlib import Path
import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="stpyvista",
    version="0.0.8",
    author="Edwin S",
    author_email="esaavedrac@u.northwestern.edu",
    description="Streamlit component that allows you to visualize pyvista 3D visualizations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    package_data={'stpyvista': ['frontend/*']},
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.8",
    install_requires=["streamlit>=1.18", "jinja2", "panel"],
)
