
import pytest

@pytest.mark.dependency()
def test_conversion_from_py(tmp_path, capsys):
    import os
    cwd = os.path.join(os.path.dirname(__file__),'temp')

    
    title_file = os.path.join(cwd, 'title.txt')
    with open(title_file,'w') as f:
        f.write('Title')
    
    data_file = os.path.join(cwd, 'data.csv')
    with open(data_file,'w') as f:
        for i in range(-5,10):
            f.write('{:10d}, {:10d}\n'.format(i, i**2))
    

    script_file = os.path.join(cwd, 'packing.py')
    
    content = b"""
import pypdfplot.backend.unpack
import matplotlib.pyplot as plt

with open('title.txt', 'r') as f:
    title = f.read()

x = []
y = []
with open('data.csv', 'r') as f:
    for line in f:
        x0, y0 = map(int,line.split(','))
        x.append(x0)
        y.append(y0)

plt.plot(x,y)
plt.title(title)
plt.savefig('packing.pdf',
            pack_list=[
                'title.txt',
                'data.csv'],
            cleanup=False,
                )
"""
    
    with open(script_file, 'wb') as f:
        f.write(content)

    assert os.path.exists(title_file)
    assert os.path.exists(data_file)
    assert os.path.exists(script_file)

    from sys import executable
    from subprocess import run
    result = run(
        [executable, 'packing.py'],
        cwd=cwd,         
        capture_output=True, 
        text=True
    )
        
    pypdf_file = os.path.join(cwd, 'packing.pdf')
    
    # print(result.stdout)
    
    assert     os.path.exists(title_file)
    assert     os.path.exists(data_file)
    assert     os.path.exists(script_file)
    assert     os.path.exists(pypdf_file)


@pytest.mark.dependency(depends=['test_conversion_from_py'])
def test_unpack_from_pypdf(tmp_path, capsys):
    import os
    cwd = os.path.join(os.path.dirname(__file__),'temp')

    title_file = os.path.join(cwd, 'title.txt')
    data_file = os.path.join(cwd, 'data.csv')
    script_file = os.path.join(cwd, 'packing.py')
    pypdf_file = os.path.join(cwd, 'packing.pdf')

    with open(title_file,'r') as f:
        title = f.read()
        
    with open(data_file,'r') as f:
        data = f.read()
        
    with open(script_file,'r') as f:
        script = f.read()
        
    # Edit script:    
    with open(pypdf_file,'rb') as f:
        buf = f.read()
    
    #Find False value
    i = buf.find(b'False')
    assert i >= 0
    
    #Replace it with False:
    buf = buf[:i] + b'True' + buf[i+len(b'False'):]
    with open(pypdf_file, 'wb') as f:
        f.write(buf)

    from sys import executable
    from subprocess import run
    result = run(
        [executable, 'packing.pdf'],
        cwd=cwd,         
        capture_output=True, 
        text=True
    )
    
    assert not os.path.exists(title_file)
    assert not os.path.exists(data_file)
    assert not os.path.exists(script_file)
    assert os.path.exists(pypdf_file)
    
    # Edit script:    
    with open(pypdf_file,'rb') as f:
        buf = f.read()
    
    #Find True value
    i = buf.find(b'True')
    assert i >= 0
    
    #Replace it with False:
    buf = buf[:i] + b'False' + buf[i+len(b'True'):]
    with open(pypdf_file, 'wb') as f:
        f.write(buf)

    from sys import executable
    from subprocess import run
    result = run(
        [executable, 'packing.pdf'],
        cwd=cwd,         
        capture_output=True, 
        text=True
    )
    
    assert     os.path.exists(title_file)
    assert     os.path.exists(data_file)
    assert     os.path.exists(script_file)
    assert     os.path.exists(pypdf_file)
    
    with open(title_file,'r') as f:
        title2 = f.read()
    assert title == title2
    
    with open(data_file,'r') as f:
        data2 = f.read()
    assert data == data2
    
    with open(script_file,'r') as f:
        script2 = f.read()
    assert script == script2