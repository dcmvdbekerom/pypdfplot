import pytest

def test_saved_pdf():
    
    from pypdfplot import fix_pypdf
    import os
    cwd = os.path.dirname(__file__)
    in_fname = os.path.join(cwd,'testfiles', 'severed_pypdf.pdf')
    out_fname = os.path.join(cwd,'temp','compliant_pypdf.pdf')
    
    if os.path.exists(out_fname):
        os.remove(out_fname)

    fix_pypdf(in_fname, out_fname)
    
    assert os.path.exists(out_fname)
    #TODO: Technically we should test if they work as well..
    os.remove(out_fname)


@pytest.mark.filterwarnings("ignore:/PyFile keyword")    
def test_edited_saved_pdf():
    from pypdfplot import fix_pypdf
    import os
    
    cwd = os.path.dirname(__file__)
    in_fname = os.path.join(cwd,'testfiles', 'severed_pypdf2.pdf')
    out_fname = os.path.join(cwd,'temp','compliant_pypdf2.pdf')
    
    if os.path.exists(out_fname):
        os.remove(out_fname)

    fix_pypdf(in_fname,out_fname)
    
    assert os.path.exists(out_fname)
    #TODO: Technically we should test if they work as well..
    os.remove(out_fname)
    