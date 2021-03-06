# Copyright 2008-2011 Nokia Networks
# Copyright 2011-2016 Ryan Tomac, Ed Manlove and contributors
# Copyright 2016-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from SeleniumLibrary.base import ContextAware


class TableElementFinder(ContextAware):

    def __init__(self, ctx):
        ContextAware.__init__(self, ctx)
        self._locator_suffixes = {
            ('css', 'default'): [''],
            ('css', 'content'): [''],
            ('css', 'header'): [' th'],
            ('css', 'footer'): [' tfoot td'],
            ('css', 'row'): [' tr:nth-child(%s)'],
            ('css', 'last-row'): [' tr:nth-last-child(%s)'],
            ('css', 'col'): [' tr td:nth-child(%s)', ' tr th:nth-child(%s)'],
            ('css', 'last-col'): [' tr td:nth-last-child(%s)', ' tr th:nth-last-child(%s)'],

            ('jquery', 'default'): [''],
            ('jquery', 'content'): [''],
            ('jquery', 'header'): [' th'],
            ('jquery', 'footer'): [' tfoot td'],
            ('jquery', 'row'): [' tr:nth-child(%s)'],
            ('jquery', 'col'): [' tr td:nth-child(%s)', ' tr th:nth-child(%s)'],

            ('sizzle', 'default'): [''],
            ('sizzle', 'content'): [''],
            ('sizzle', 'header'): [' th'],
            ('sizzle', 'footer'): [' tfoot td'],
            ('sizzle', 'row'): [' tr:nth-child(%s)'],
            ('sizzle', 'col'): [' tr td:nth-child(%s)', ' tr th:nth-child(%s)'],

            ('xpath', 'default'): [''],
            ('xpath', 'content'): ['//*'],
            ('xpath', 'header'): ['//th'],
            ('xpath', 'footer'): ['//tfoot//td'],
            ('xpath', 'row'): ['//tr[%s]//*'],
            ('xpath', 'last-row'): [' //tbody/tr[position()=last()-(%s-1)]'],
            ('xpath', 'col'): ['//tr//*[self::td or self::th][%s]'],
            ('xpath', 'last-col'): [' //tbody/tr/td[position()=last()-(%s-1)]', ' //tbody/tr/td[position()=last()-(%s-1)]']
        }

    def find(self, table_locator):
        locators = self._parse_table_locator(table_locator, 'default')
        return self._search_in_locators(locators, None)

    def find_by_content(self, table_locator, content):
        locators = self._parse_table_locator(table_locator, 'content')
        return self._search_in_locators(locators, content)

    def find_by_header(self, table_locator, content):
        locators = self._parse_table_locator(table_locator, 'header')
        return self._search_in_locators(locators, content)

    def find_by_footer(self, table_locator, content):
        locators = self._parse_table_locator(table_locator, 'footer')
        return self._search_in_locators(locators, content)

    def find_by_row(self, table_locator, row, content):
        location_method = "row"
        row = str(row)
        if row[0] == "-":
            row = row[1:]
            location_method = "last-row"
        locators = self._parse_table_locator(table_locator, location_method)
        locators = [locator % str(row) for locator in locators]
        return self._search_in_locators(locators, content)

    def find_by_col(self, table_locator, col, content):
        location_method = "col"
        col = str(col)
        if col[0] == "-":
            col = col[1:]
            location_method = "last-col"
        locators = self._parse_table_locator(table_locator, location_method)
        locators = [locator % str(col) for locator in locators]
        return self._search_in_locators(locators, content)

    def _parse_table_locator(self, table_locator, location_method):
        if table_locator.startswith('xpath='):
            table_locator_type = 'xpath'
        elif table_locator.startswith('jquery=') or table_locator.startswith('sizzle='):
            table_locator_type = 'sizzle'
        else:
            if not table_locator.startswith('css='):
                table_locator = "css=table#%s" % table_locator
            table_locator_type = 'css'
        locator_suffixes = self._locator_suffixes[(table_locator_type, location_method)]
        return map(
            lambda locator_suffix: table_locator + locator_suffix,
            locator_suffixes)

    def _search_in_locators(self, locators, content):
        for locator in locators:
            elements = self.element_finder.find(locator, first_only=False,
                                                required=False)
            for element in elements:
                if content is None:
                    return element
                element_text = element.text
                if element_text and content in element_text:
                    return element
        return None
