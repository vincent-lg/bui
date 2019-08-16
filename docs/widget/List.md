# List in [widget/list:9](../raw/widget/list.html#L9)

The generic list widget.

A list is to represent a choice given to the user, with
several possible choices.  The user should select 0, 1 or more
depending on the list type.  This list should be defined
inside a [window](../layout/tag/window.md) tag.

This is a generic widget which will be converted into a specific widget,
depending on the used GUI toolkit.

## Class summary

This class offers 2 properties.

| Property | Get | Set |
| -------- | --- | --- |
| [choices](#choices) | Return the list choices. | Modify the choices in the list. |
| [selected](#selected) | Return the currently-selected choice ID or position. | Change the selected label. |

This class offers 5 methods.

| Method | Signature | Description |
| ------ | --------- | ----------- |
| [add_choice](#add_choice) | `add_choice(choice: Union[Any, Tuple[Hashable, Any]])` | Add a new choice at the end of the list. |
| [create_specific](#create_specific) | `create_specific()` | Create the specific widget, using the `specific_package` attribute. |
| [remove_choice](#remove_choice) | `remove_choice(identifier: Any)` | Remove a choice in the list. |
| [schedule](#schedule) | `schedule(coroutine)` | Schedule the specified coroutine in the main event loop. |
| [update_choice](#update_choice) | `update_choice(i, choice)` | Update the specified choice. |

## Properties

### choices

This property can get and be set.

#### Get

[See the source code](../raw/widget/list.html#L88)

Return the list choices.

#### Set

[See the source code](../raw/widget/list.html#L93)

Modify the choices in the list.

Args:
    choices (iterable): a list of choicess, where each choice can
            be a label (preferably a str) or a tuple
            (identifier, label) where identifier is hashable
            (a string is often preferred).

### selected

This property can get and be set.

#### Get

[See the source code](../raw/widget/list.html#L131)

Return the currently-selected choice ID or position.

#### Set

[See the source code](../raw/widget/list.html#L136)

Change the selected label.

## Methods

### add_choice

`add_choice(self, choice: Union[Any, Tuple[Hashable, Any]])`

[See the source code](../raw/widget/list.html#L151)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `List` |  |
| choice | `Union[Any, Tuple[Hashable, Any]]` |  |

Add a new choice at the end of the list.

Args:
    choice (Choice): a choice, either a choice label (probably
            a string) or a tuple of (choice identifier, choice label)
            where both may be strings.  The choice identifier,
            if specified, should be hashable.  The label
            has no constraint (if it's not a string, then
            str() will be called on it).

Note:
    The label is what the user will see in the list, the
    identifier will identify the user selection for the
    developer.  If you don't specify any identifier,
    the choice position in the list will be used.

### create_specific

`create_specific(self)`

[See the source code](../raw/widget/list.html#L30)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `List` |  |

Create the specific widget, using the `specific_package` attribute.

If the specific object has already been created, don't recreate it and
raise no exception.

### remove_choice

`remove_choice(self, identifier: Any)`

[See the source code](../raw/widget/list.html#L187)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `List` |  |
| identifier | `Any` |  |

Remove a choice in the list.

Args:
    identifier (Any): the choice identifier or int position.

### schedule

`schedule(self, coroutine)`

[See the source code](../raw/widget/list.html#L75)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `List` |  |
| coroutine | *Not set* |  |

Schedule the specified coroutine in the main event loop.

### update_choice

`update_choice(self, i, choice)`

[See the source code](../raw/widget/list.html#L182)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `List` |  |
| i | *Not set* |  |
| choice | *Not set* |  |

Update the specified choice.