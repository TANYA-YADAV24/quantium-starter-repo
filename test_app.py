import pytest 
from dash.testing.application_runners import import_app 
 
@pytest.fixture 
def app(dash_duo): 
    app = import_app("app") 
    dash_duo.start_server(app) 
    return dash_duo 
 
def test_header_is_present(app): 
    app.wait_for_element("h1", timeout=10) 
    header = app.find_element("h1") 
    assert header is not None 
    assert "Pink Morsel Sales Analysis" in header.text 
 
def test_visualisation_is_present(app): 
    app.wait_for_element("#sales-chart", timeout=10) 
    graph = app.find_element("#sales-chart") 
    assert graph is not None 
 
def test_region_picker_is_present(app): 
    app.wait_for_element("#region-filter", timeout=10) 
    region_picker = app.find_element("#region-filter") 
    assert region_picker is not None 
