def test_import_agents():
    """Test that agent modules can be imported"""
    try:
        from agents import story_generator
        from agents import panel_generator
        from agents import bubble_drawer
        assert True
    except ImportError as e:
        assert False, f"Import failed: {e}"
