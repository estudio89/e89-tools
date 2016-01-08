class MockObject(object):
    ''' Class that allows mocking an object's attributes or methods.
        It receives a dictionary that contains attributes and its mocked values.
        It works with nested objects as well. For example, if you have object "foo" with
        attribute "bar" and you want to mock bar's method "mock", all you have to do is pass
        the dictionary {"mock":"mock_value"} to the constructor.'''

    def __init__(self, mock_attrs):
        self.mock_attrs = mock_attrs

    def __getattr__(self, attr_name):
        if self.mock_attrs.has_key(attr_name):
            return self.mock_attrs[attr_name]
        else:
            return MockObject(self.mock_attrs)
