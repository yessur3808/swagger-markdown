import markdown
import unittest
from swaggermarkdown import SwaggerExtension

style = '''
<style>
  body {
    font-size: 16px;
    font-family: sans-serif;
  }
  table {
    border-collapse: collapse;
    margin: 30px;
    min-width: 400px;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
  }
  th,
  td {
      padding: 12px 15px;
  }
  tbody tr {
    border-bottom: 1px solid #dddddd;
  }

  tbody tr:nth-of-type(even) {
      background-color: #f3f3f3;
  }

  .sw-label {
    color: #666;
    display: inline-block;
    min-width: 80px;
    text-align: right;
  }
</style>
'''

class TestSwaggerExtension(unittest.TestCase):

    def test_instanciate_extension(self):
        text = 'some text'
        self.assertEqual('<p>'+text+'</p>', markdown.markdown(text, extensions=['swaggermarkdown']))
    

    def test_instanciate_extension_with_file(self):
        md = markdown.Markdown(extensions=[SwaggerExtension(file='test_swagger.json')])
        text = 'some text'
        self.assertEqual('<p>'+text+'</p>', md.convert(text))

    def test_swagger_include(self):
        md = markdown.Markdown(extensions=[SwaggerExtension(file='test_swagger.json')])
        text = ':swg: FirstDefinition'
        converted = md.convert(text)
        self.assertTrue(converted.startswith('<table '))

    def test_generate_file(self):
        md = markdown.Markdown(extensions=[SwaggerExtension(file='test_swagger.json')])
        with open('test.md', 'r') as md_input:
            html = md.convert(md_input.read())
            with open("test.html", "w") as out:
              out.write(style)
              out.write(html)

    def test_swagger_explicit_file_include(self):
        md = markdown.Markdown(extensions=[SwaggerExtension()])
        text = ':swg: test_swagger.json FirstDefinition'
        converted = md.convert(text)
        self.assertTrue(converted.startswith('<table '))

    def test_data_present(self):
        md = markdown.Markdown(extensions=[SwaggerExtension()])
        text = ':swg: test_swagger.json FirstDefinition'
        converted = md.convert(text)
        self.assertIn('Some example text', converted)
        self.assertIn('example', converted)
        self.assertIn('2050', converted)
        self.assertIn('1999', converted)
        self.assertIn('arrayOfStrings', converted)
        self.assertIn('minItems', converted)
        self.assertIn('123', converted)
        self.assertIn('hello world', converted)
        self.assertIn('<strong>name</strong>', converted)
        self.assertIn('array of string', converted)
        self.assertIn('<a href="#/definitions/SecondDefinition">SecondDefinition</a>', converted)
        self.assertIn('integer int32', converted)
        self.assertIn('arrayOfObject</strong>[0].id', converted)

    def test_2_definition(self):
        md = markdown.Markdown(extensions=[SwaggerExtension(file='test_swagger.json')])
        text = '''
:swg: test_swagger.json FirstDefinition
:swg: SecondDefinition
'''
        converted = md.convert(text)
        self.assertIn('Some example text', converted)
        self.assertIn('another def', converted)

    def test_definitionsUrlRoot(self):
        md = markdown.Markdown(extensions=[SwaggerExtension(definitionsUrlRoot='/types')])
        text = ':swg: test_swagger.json FirstDefinition'
        converted = md.convert(text)
        self.assertIn('<a href="/types#/definitions/SecondDefinition">SecondDefinition</a>', converted)


if __name__ == '__main__':
    unittest.main()