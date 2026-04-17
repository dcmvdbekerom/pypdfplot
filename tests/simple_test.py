
import pytest

@pytest.mark.dependency()
def test_conversion_from_py(tmp_path, capsys):
    import os
    cwd = os.path.join(os.path.dirname(__file__), 'temp')

    script_file = os.path.join(cwd, 'simple.py')
    
    content = b"""
import pypdfplot.backend
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(-10,20,0.1)
y = x**2

plt.plot(x,y)
plt.savefig('simple.pdf')
"""
    
    with open(script_file, 'wb') as f:
        f.write(content)

    assert os.path.exists(script_file)

    from sys import executable
    from subprocess import run
    result = run(
        [executable, 'simple.py'],
        cwd=cwd,         
        capture_output=True, 
        text=True
    )
    
    pypdf_file = os.path.join(cwd, 'simple.pdf')
    
    # with capsys.disabled():
    # print(f"\nTemp path:\n{tmp_path}")
    # print(result.stdout)

    assert not os.path.exists(script_file)
    assert     os.path.exists(pypdf_file)


@pytest.mark.dependency(depends=["test_conversion_from_py"])
def test_header_trailer(tmp_path):
    import os
    cwd = os.path.join(os.path.dirname(__file__), 'temp')
    
    with open(os.path.join(cwd, 'simple.pdf'), 'rb') as f:
        fsize = f.seek(0,2)
        f.seek(0, 0)
        buf = f.read()
    
    assert buf[:5] == b'#%PDF'
    
    ## Find PDF EOF marker
    i = buf.rfind(b'%%EOF')
    assert i >= 0
    
    ## Compare reported filesize with actual filesize
    # buf = buf[i:]
    size_str = buf[i:].splitlines()[1].split()[0]
    assert int(size_str) == fsize
    
    ## Check for PyPDF marker
    j = buf[i:].rfind(b'PyPDF')
    assert j == 20


@pytest.mark.dependency(depends=["test_conversion_from_py"])
def test_conversion_from_pypdf(tmp_path, capsys):
    import os
    cwd = os.path.join(os.path.dirname(__file__), 'temp')

    from sys import executable
    from subprocess import run
    result = run(
        [executable, 'simple.pdf'],
        cwd=cwd,         
        capture_output=True, 
        text=True
    )
    

    assert os.path.exists(os.path.join(cwd, 'simple.pdf'))

@pytest.mark.dependency(depends=["test_conversion_from_pypdf"])    
def test_header_trailer2(tmp_path):
    test_header_trailer(tmp_path)