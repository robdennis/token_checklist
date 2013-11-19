""":mod:`my_module.metadata` --- Project metadata

Given a List of Magic: The Gathering Card names, \
return a list of tokens produced
"""

# The package name, which is also the "UNIX name" for the project.
package = 'token_checklist'
project = 'Token Checklist'
project_no_spaces = project.replace(' ', '')
version = '0.1.0'
description = ('Given a List of Magic: The Gathering Card names, '
               'return a list of tokens produced')
authors = ['Rob Dennis']
authors_string = ', '.join(authors)
emails = ['rdennis+{}@gmail.com'.format(project)]
license = 'MIT'
copyright = '2013 ' + authors_string
url = 'https://github.com/robdennis/token_checklist'
