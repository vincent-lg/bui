# RadioButton in [widget/radio:7](../raw/widget/radio.html#L7)

The generic radio button widget.

A radio button is to represent a group of choices, each choice being
a button.  Selecting one forces the other ones to get unselected.
This widget needs to be inside a [window](../layout/tag/window.md)
tag.  It should have at least two choices, but you can set them
initially with the [choice tag]../layout/tag/choice.md) or later
with the `choices` property on this widget.

This is a generic widget which will be converted into a specific widget,
depending on the used GUI toolkit.

## Class summary

This class offers 2 properties.

| Property | Get | Set |
| -------- | --- | --- |
| [choices](#choices) | Return the current choices. | Modify the radio button choices. |
| [selected](#selected) | Return the ID of the selected choice. | Change the selected choice. |

This class offers 2 methods.

| Method | Signature | Description |
| ------ | --------- | ----------- |
| [create_specific](#create_specific) | `create_specific()` | Create the specific widget, using the `specific_package` attribute. |
| [schedule](#schedule) | `schedule(coroutine)` | Schedule the specified coroutine in the main event loop. |

## Properties

### choices

This property can get and be set.

#### Get

[See the source code](../raw/widget/radio.html#L47)

Return the current choices.

#### Set

[See the source code](../raw/widget/radio.html#L52)

Modify the radio button choices.

Args:
    choices (iterable): an iterable containing choices, each
            choice being a tuple with two elements (both of
            `str`): the choice ID and the choice label.

### selected

This property can get and be set.

#### Get

[See the source code](../raw/widget/radio.html#L79)

Return the ID of the selected choice.

#### Set

[See the source code](../raw/widget/radio.html#L84)

Change the selected choice.

## Methods

### create_specific

`create_specific(self)`

[See the source code](../raw/widget/radio.html#L30)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `RadioButton` |  |

Create the specific widget, using the `specific_package` attribute.

If the specific object has already been created, don't recreate it and
raise no exception.

### schedule

`schedule(self, coroutine)`

[See the source code](../raw/widget/radio.html#L75)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `RadioButton` |  |
| coroutine | `inspect._empty` |  |

Schedule the specified coroutine in the main event loop.