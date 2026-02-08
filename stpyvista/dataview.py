from io import StringIO
import streamlit as st
from pyvista import DataSet


def dataview(obj: DataSet):
    """
    Renders the HTML representation of a Pyvista/VTK dataset.

    Parameters
    ----------
    element: pv.DataSet
        Pyvista element with some data to show.

    Returns
    -------
    None
    """
    import xml.dom.minidom

    def assemble_details(title: str, table: str) -> str:
        if title.lower() == "header":
            title = type(obj).__name__

        return f"<details open><summary><em>{title}</em></summary>{table}</details>"

    try:
        # Look up an HTML representation and arange in details tags

        dom = xml.dom.minidom.parseString(obj._repr_html_())
        tables = dom.getElementsByTagName("table")

        css = """
            <style>
            details {
                padding: 6px;
                margin-bottom: 5px; 
                border: 1px solid #eeeeee;
                background-color: transparent;
                border-radius: 10px;
            }
            summary {
                background-color: transparent;
                opacity: 60%;
                padding: 5px;
            }
            summary::marker {
                color: purple;
                font-size: 1.1em;
            }
            </style>
        """

        html = StringIO("""<div class="stpv-dataview">""")

        if len(tables) == 1:
            html.write(assemble_details(type(obj).__name__, tables[0].toprettyxml()))

        else:
            headers = (
                dom.getElementsByTagName("table")[0]
                .getElementsByTagName("tr")[0]
                .getElementsByTagName("th")
            )

            for title, table in zip(headers, tables[1:]):
                html.write(
                    assemble_details(title.firstChild.nodeValue, table.toprettyxml())
                )

        html.write(css + "</div>")

        # Render in streamlit
        st.html(html.getvalue())

    except AttributeError:
        # Defaults to streamlit's write function
        st.write(obj)
