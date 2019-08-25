# Blind User Interface examples

BUI provides simple examples you can run to test the application and see how the code works.  If you have cloned the repository, you will find these examples in the `example` directory.  You will also find them online (see below).

## Installation

These examples are standalone examples, meaning you just need to install BUI and enable the feature to run these examples.  To do so, run `pip`:

    pip install bui[demo]

Specifying `[demo]` will install additional packages that may be required by one example.  Preferably, run this command in a virtual environment.  Then, head over to an example.

## Run an example

Assuming you are interested in the [download example](download.md), and you would like to test it: nothing easier!

Open the [download.py](download.md) file.  If you have cloned the repository, you will find it in the `example` directory ([see it on Github](https://github.com/vincent-lg/bui/blob/master/example/download.py).  If not, open the [example page for the download app](download.md).  Above is a quick explanation of the example, read it or skip it.  Below you will see the source code.  Copy the entire source code and paste it in a file (preferably `download.py` to be consistent).  Then simply run it:

    python download.py

And you should see the example appear.

## List of examples

| Example                        | Description                          |
| ------------------------------ | ------------------------------------ |
| [download.py](download.md)     | Show a window with a download queue. |
