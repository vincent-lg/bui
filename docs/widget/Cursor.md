# Cursor in [widget/text:98](../raw/widget/text.html#L98)

Class to represent a cursor in a text field.

A cursor object is created when a text widget is created.  This cursor
object will be updated whenever the need arises.

## Class summary

This class offers 8 properties.

| Property | Get | Set |
| -------- | --- | --- |
| [at_begin](#at_begin) | Return True if the cursor is at the beginning of the text field. | **Can't write** |
| [at_end](#at_end) | Return True if the cursor is at the end of the text field. | **Can't write** |
| [col](#col) | Return the current column (horizontal position of the cursor). | **Can't write** |
| [line](#line) | Return the current line of text. | **Can't write** |
| [lineno](#lineno) | Return the current line number (vertical position of the cursor). | **Can't write** |
| [pos](#pos) | Return the current position as an indice. | **Can't write** |
| [text_after](#text_after) | Return the text after the cursor. | **Can't write** |
| [text_before](#text_before) | Return the text before the cursor. | **Can't write** |

This class offers 1 method.

| Method | Signature | Description |
| ------ | --------- | ----------- |
| [move](#move) | `move(pos: int, col: Optional[int] = None)` | Move the cursor. |

## Properties

### at_begin

This property can only get (read-only).

#### Get

[See the source code](../raw/widget/text.html#L129)

Return True if the cursor is at the beginning of the text field.

### at_end

This property can only get (read-only).

#### Get

[See the source code](../raw/widget/text.html#L134)

Return True if the cursor is at the end of the text field.

### col

This property can only get (read-only).

#### Get

[See the source code](../raw/widget/text.html#L124)

Return the current column (horizontal position of the cursor).

### line

This property can only get (read-only).

#### Get

[See the source code](../raw/widget/text.html#L149)

Return the current line of text.

### lineno

This property can only get (read-only).

#### Get

[See the source code](../raw/widget/text.html#L119)

Return the current line number (vertical position of the cursor).

### pos

This property can only get (read-only).

#### Get

[See the source code](../raw/widget/text.html#L114)

Return the current position as an indice.

### text_after

This property can only get (read-only).

#### Get

[See the source code](../raw/widget/text.html#L144)

Return the text after the cursor.

### text_before

This property can only get (read-only).

#### Get

[See the source code](../raw/widget/text.html#L139)

Return the text before the cursor.

## Methods

### move

`move(self, pos: int, col: Optional[int] = None)`

[See the source code](../raw/widget/text.html#L154)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Cursor` |  |
| pos | `int` |  |
| col | `Optional[int]` | `None` |

Move the cursor.

This method accepts two possible signatures:
    move(position): moves the cursor to the absolute position
            in the text.
    move(lineno, col): move the cursor at a given line number
            and column number.