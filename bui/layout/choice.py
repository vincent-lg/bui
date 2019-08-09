"""Choice object represented in layout."""

from bui.layout.attr import Attr
from bui.layout.component import Component

class Choice(Component):

    """
    Create a choice inside of a radio tag.

    A choice is a layout component of a [radio](./radio.md) tag.  A
    radio group should have at least two choices.  Choices
    can be defined in the layout, or through the
    [RadioButton.choices](../../widget/RadioButton.md#choices) property.

    ```
    <window title="Radio group demonstration">
      <radio id=actions x=2 y=4>
        <choice>One</choice>
        <choice>Two</choice>
        <choice id=nothing>Do nothing</choice>
      </radio>
    </window>
    ```

    ## Attributes

    | Name         | Required | Description              | Example     |
    | ------------ | -------- | ------------------------ | ----------- |
    | `id`         | no       | The choice identifier    | `<choice    |
    |              |          | (ID). If not set, use    | id=one>`    |
    |              |          | the label specified as   |             |
    |              |          | data of the `<choice>`   |             |
    |              |          | tag.                     |             |

    See also the [radio](./radio.md) tag to set the radio button group
    in the layout.

    Specify the label of the choice as data of this tag.  This is a
    translatable data, it can contain data to be translated.  In this case,
    specifying an ID is required.

    If the identifier is not set, use the label specified in the data of
    the tag.  For instance:

        <choice>Install it again</choice>

    Will result in a choice of ID "install_it_again" (lowercase).

    ## Data

    The choice isn't a proper widget by itself.  It exists in the layout,
    but isn't linked to a generic widget.  Interacting on a single choice
    is not possible with this object, rather, see the
    [radio tag](./radio.md).  Therefore, it has no attribute or methof
    of its own.

    ## Controls

    The choice isn't a proper widget by itself.  It exists in the layout,
    but isn't linked to a generic widget.  Interacting on a single choice
    is not possible with this object, rather, see the
    [radio tag](./radio.md).  Therefore, it has no control of its own.

    """

    tag_name = "choice"
    attrs = (
        Attr("id", help="The widget identifier", default=""),
    )
    must_have_data = True
    has_widget = False

    def __init__(self, layout, parent, id):
        super().__init__(layout, parent)
        self.id = id

    def complete(self):
        """Complete the tag, when all the layout has been set."""
        if not self.id:
            self.id = self.deduce_id(self.data)
