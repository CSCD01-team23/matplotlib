import difflib
import subprocess
import sys
from pathlib import Path

import pytest

import matplotlib as mpl
from matplotlib import pyplot as plt


def test_pyplot_up_to_date():
    gen_script = Path(mpl.__file__).parents[2] / "tools/boilerplate.py"
    if not gen_script.exists():
        pytest.skip("boilerplate.py not found")
    orig_contents = Path(plt.__file__).read_text()
    try:
        subprocess.run([sys.executable, str(gen_script)], check=True)
        new_contents = Path(plt.__file__).read_text()

        if orig_contents != new_contents:
            diff_msg = '\n'.join(
                difflib.unified_diff(
                    orig_contents.split('\n'), new_contents.split('\n'),
                    fromfile='found pyplot.py',
                    tofile='expected pyplot.py',
                    n=0, lineterm=''))
            pytest.fail(
                "pyplot.py is not up-to-date. Please run "
                "'python tools/boilerplate.py' to update pyplot.py. "
                "This needs to be done from an environment where your "
                "current working copy is installed (e.g. 'pip install -e'd). "
                "Here is a diff of unexpected differences:\n%s" % diff_msg
            )
    finally:
        Path(plt.__file__).write_text(orig_contents)


def test_pyplot_box():
    fig, ax = plt.subplots()
    plt.box(False)
    assert not ax.get_frame_on()
    plt.box(True)
    assert ax.get_frame_on()
    plt.box()
    assert not ax.get_frame_on()
    plt.box()
    assert ax.get_frame_on()


def test_stackplot_smoke():
    # Small smoke test for stackplot (see #12405)
    plt.stackplot([1, 2, 3], [1, 2, 3])


def test_nrows_error():
    with pytest.raises(TypeError):
        plt.subplot(nrows=1)
    with pytest.raises(TypeError):
        plt.subplot(ncols=1)


def test_lines_dark_background_default():
    plt.style.use('dark_background')
    plt.figure()
    with mpl.rc_context({'lines.color': 'white'}):
        hline = plt.hlines(0.5, 0, 1)
        vline = plt.vlines(0.5, 0, 1)
    actualh = hline.get_color()
    expectedh = mpl.colors.to_rgba_array(mpl.rcParams['lines.color'])
    actualv = vline.get_color()
    expectedv = mpl.colors.to_rgba_array(mpl.rcParams['lines.color'])
    assert mpl.colors.same_color(actualh, expectedh)
    assert mpl.colors.same_color(vline.get_color(), expectedv)


def test_lines_dark_background():
    plt.style.use('dark_background')
    plt.figure()
    with mpl.rc_context({'lines.color': 'white'}):
        hline = plt.hlines(0.5, 0, 1, colors='red')
        vline = plt.vlines(0.5, 0, 1, colors='green')
    actualh = hline.get_color()
    expectedh = mpl.colors.to_rgba_array('red')
    actualv = vline.get_color()
    expectedv = mpl.colors.to_rgba_array('green')
    assert mpl.colors.same_color(actualv, expectedv)
    assert mpl.colors.same_color(actualv, expectedv)


def test_lines_white_background_default():
    plt.figure()
    hline = plt.hlines(0.5, 0, 1)
    vline = plt.vlines(0.5, 0, 1)
    actualh = hline.get_color()
    expectedh = mpl.colors.to_rgba_array(mpl.rcParams['lines.color'])
    actualv = vline.get_color()
    expectedv = mpl.colors.to_rgba_array(mpl.rcParams['lines.color'])
    assert mpl.colors.same_color(actualh, expectedh)
    assert mpl.colors.same_color(actualv, expectedv)


def test_lines_white_background():
    plt.figure()
    with mpl.rc_context({'lines.color': 'white'}):
        hline = plt.hlines(0.5, 0, 1, colors='k')
        vline = plt.vlines(0.5, 0, 1, colors='red')
    actualh = hline.get_color()
    expectedh = mpl.colors.to_rgba_array('k')
    actualv = vline.get_color()
    expectedv = mpl.colors.to_rgba_array('red')
    assert mpl.colors.same_color(actualh, expectedh)
    assert mpl.colors.same_color(actualv, expectedv)
