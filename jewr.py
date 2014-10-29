"""
JEWR the java file management tool

Copyright (C) 2014 Harri Savolainen

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

@author: Harri Savolainen
@copyright: Copyright 2014, Harri Savolainen
@license: GPLv3
@version: 1.0
@maintainer: Harri Savolainen
@email: harri.savolainen@gmail.com
@status: Production

"""
import zipfile
import sys
import os
import argparse
import tempfile
import shutil


class JarEarWarRar(object):
    """docstring for ClassName"""
    known_types = ['.jar', '.ear', '.rar', '.war']
    tmp_dir = ""
    destination_dir = None

    # pylint: disable=no-self-use
    def extract_file(self, file_name, target_file, target_dir):
        """docstring for Method"""
        contents = zipfile.ZipFile(file_name, 'r')
        files = [elem for elem in contents.namelist() if not elem.endswith(
            os.sep)]

        if target_file not in files:
            raise IOError("'" + target_file + "' not found in '" + file_name +
                          "'")
        contents.extract(target_file, target_dir)
        return True

    def parse_java_path(self, java_archive_path):
        """docstring for Method"""
        split_token = "\n"
        for jtype in self.known_types:
            java_archive_path = java_archive_path.replace(jtype + os.sep,
                                                          jtype + os.sep +
                                                          split_token)
        return java_archive_path.split(os.sep + split_token)

    def set_temp_dir(self, temp_dir=None):
        """docstring for Method"""
        self.clean_tmp_dir()
        if temp_dir is None:
            if os.access('/dev/shm', os.W_OK):
                self.tmp_dir = tempfile.mkdtemp(suffix='', prefix='tmp',
                                                dir="/dev/shm")
            else:
                self.tmp_dir = tempfile.mkdtemp()
        else:
            self.tmp_dir = tempfile.mkdtemp(suffix='', prefix='tmp',
                                            dir=temp_dir)

        return self.tmp_dir

    def clean_tmp_dir(self):
        """docstring for Method"""
        if self.tmp_dir is not "":
            if os.access(self.tmp_dir, os.W_OK):
                shutil.rmtree(self.tmp_dir)
        return True

    def set_destination_dir(self, destination_dir=None):
        """docstring for Method"""
        if destination_dir is None:
            self.destination_dir = os.getcwd()
        else:
            self.destination_dir = destination_dir
        if not os.access(self.destination_dir, os.W_OK):
            raise IOError("error: " + self.destination_dir +
                          " is not writeable.")
        return True

    def return_file(self, file_path):
        """docstring for Method"""
        shutil.move(file_path, self.destination_dir)
        return True

    def process_file(self, java_archive_path):
        """docstring for Method"""
        java_file_list = self.parse_java_path(java_archive_path)
        first_element = 0
        last_element = len(java_file_list)-1
        for i in range(0, len(java_file_list)):
            # First element
            if i == first_element:
                # And same time the second last (two elements in array)
                if i+1 == last_element:
                    subdir = self.tmp_dir + os.sep + str(i)
                    self.extract_file(java_file_list[i], java_file_list[i+1],
                                      subdir)
                    self.return_file(subdir + os.sep +
                                     java_file_list[i+1])

                # More than two elements in a array
                else:
                    subdir = self.tmp_dir + os.sep + str(i)
                    os.mkdir(subdir)
                    self.extract_file(java_file_list[i], java_file_list[i+1],
                                      subdir)

            # All the next elements until second last element
            if i > first_element and i < last_element:
                nsubdir = self.tmp_dir + os.sep + str(i)
                psubdir = self.tmp_dir + os.sep + str(i-1)
                # Second last element
                if i+1 == last_element:
                    self.extract_file(psubdir + os.sep + java_file_list[i],
                                      java_file_list[i+1],
                                      nsubdir)
                    self.return_file(nsubdir + os.sep +
                                     java_file_list[i+1])
                # Other element than second last
                else:
                    os.mkdir(nsubdir)
                    self.extract_file(psubdir + os.sep + java_file_list[i],
                                      java_file_list[i+1], nsubdir)
        return True

    def __init__(self):
        """docstring for Method"""
        pass

    def __del__(self):
        """docstring for Method"""
        self.clean_tmp_dir()


#
# Hidden test suite
# Requires python unittest and mock libraries
#
def test():
    """docstring for Method"""
    import unittest
    import mock

    # pylint: disable=too-many-public-methods
    class ToolTestCases(unittest.TestCase):
        """docstring for ClassName"""

        def setUp(self):
            """docstring for Method"""
            pass

        @mock.patch('jewr.zipfile.ZipFile')
        def test_extract_file(self, mock_zipfile):
            """Testing file extraction from Java archive"""
            mock_zipfile.return_value.namelist.return_value = \
                ['foo' + os.sep, 'foo' + os.sep + 'bar.jar', 'baz.jar']
            tool = JarEarWarRar()
            # Test the sunshiny path, file is found
            tool.extract_file("foo_test.file", "foo" + os.sep + "bar.jar",
                              "/tmp")
            mock_zipfile.return_value.extract.assert_called_with(
                "foo" + os.sep + "bar.jar", '/tmp')

            # Test the requested file is not found
            self.assertRaises(IOError, tool.extract_file, "foo_test.file",
                              "foo" + os.sep + "bar2.jar", "/tmp")

            # Test the requested file is found but a directory
            self.assertRaises(IOError, tool.extract_file, "foo_test.file",
                              "foo" + os.sep, "/tmp")

        def test_parse_java_path(self):
            """Testing parsing java path and splitting to components"""
            tool = JarEarWarRar()
            # Sunshiny path
            java_archive_path = os.sep + "foo" + os.sep + "bar.ear" + os.sep +\
                "bar.jar"
            expected_parse = [os.sep + 'foo' + os.sep + 'bar.ear', 'bar.jar']
            parse_result = tool.parse_java_path(java_archive_path)
            self.assertEquals(parse_result, expected_parse)

            # Sunshiny path single item
            java_archive_path = os.sep + "foo" + os.sep + "bar.war"
            expected_parse = [os.sep + "foo" + os.sep + "bar.war"]
            parse_result = tool.parse_java_path(java_archive_path)
            self.assertEquals(parse_result, expected_parse)

        def test_temp_dir(self):
            """Testing if temp directory can be set and created properly"""
            shutil.rmtree = mock.MagicMock(return_value=True)
            tool = JarEarWarRar()

            # Sunshiny path using linux ramdisk
            os.access = mock.MagicMock(return_value=True)
            tempfile.mkdtemp = mock.MagicMock(return_value='/dev/shm/tempdir')
            tool.set_temp_dir()
            self.assertEquals(tool.tmp_dir.startswith("/dev/shm"), True)

            # Another path using default temp directory
            os.access = mock.MagicMock(return_value=False)
            tempfile.mkdtemp = mock.MagicMock(return_value='/tmp/tempdir')
            tool.set_temp_dir()
            self.assertEquals(tool.tmp_dir.startswith(tempfile.gettempdir()),
                              True)

            # Custom directory
            os.access = mock.MagicMock(return_value=False)
            tempfile.mkdtemp = mock.MagicMock(return_value='/foo/tempdir')
            tool.set_temp_dir("/foo")
            self.assertEquals(tool.tmp_dir.startswith("/foo"), True)

        def test_clean_tmp_dir(self):
            """Testing temp directory cleaning functionality"""
            tool = JarEarWarRar()

            # Sunshiny path
            os.access = mock.MagicMock(return_value=True)
            shutil.rmtree = mock.MagicMock(return_value=True)
            tempfile.mkdtemp = mock.MagicMock(return_value='/dev/shm/tempdir')
            tool.set_temp_dir()
            self.assertEquals(tool.tmp_dir.startswith("/dev/shm"), True)
            tool.clean_tmp_dir()
            # pylint: disable=maybe-no-member
            shutil.rmtree.assert_called_with('/dev/shm/tempdir')

        # pylint: disable=no-self-use
        def test_return_file(self):
            """Testing file return functionality"""
            tool = JarEarWarRar()
            os.getcwd = mock.MagicMock(return_value='/tmp/test')
            os.access = mock.MagicMock(return_value=True)
            shutil.move = mock.MagicMock(return_value=True)
            tool.set_destination_dir()
            tool.return_file('/tmp/td/2/lib/foo.properties')

            # pylint: disable=maybe-no-member
            shutil.move.assert_called_with('/tmp/td/2/lib/foo.properties',
                                           '/tmp/test')

        def test_set_destination_dir(self):
            """Testing if destination directory can be set properly"""
            tool = JarEarWarRar()
            os.getcwd = mock.MagicMock(return_value='/tmp/test')
            os.access = mock.MagicMock(return_value=True)

            # Sunshiny path with current pwd
            tool.set_destination_dir()
            self.assertEquals(tool.destination_dir, '/tmp/test')

            # Sunshiny path with dir set
            os.access = mock.MagicMock(return_value=True)
            tool.set_destination_dir('/tmp/test2')
            self.assertEquals(tool.destination_dir, '/tmp/test2')

            # Unable to write case
            os.access = mock.MagicMock(return_value=False)
            self.assertRaises(IOError, tool.set_destination_dir)

        # pylint: disable=unused-argument,
        @mock.patch.object(JarEarWarRar, 'return_file', return_value=True)
        @mock.patch.object(JarEarWarRar, 'extract_file', return_value=True)
        @mock.patch.object(JarEarWarRar, 'clean_tmp_dir', return_value=True)
        @mock.patch.object(JarEarWarRar, 'parse_java_path',
                           return_value=['bar.ear', 'foo.war', 'META-INF' +
                                         os.sep + 'lib' + os.sep + 'baz.jar',
                                         'baz.properties'])
        def test_process_file(self, mock_parse, mock_clean_tmp, mock_extract,
                              mock_return_file):
            """Testing file processing and call order"""
            # Sunshine path with many elements
            path = 'bar.ear' + os.sep + 'foo.war' + os.sep + 'META-INF' +\
                os.sep + 'lib' + os.sep + 'baz.jar' + os.sep + 'baz.properties'
            temp = '/dev/shm/tempdir'
            target = temp+'/2'
            dest_dir = '/foo'
            os.mkdir = mock.MagicMock(return_value=True)
            os.access = mock.MagicMock(return_value=True)
            shutil.move = mock.MagicMock(return_value=True)

            tool = JarEarWarRar()
            tool.set_temp_dir(temp)
            tool.set_destination_dir(dest_dir)
            tool.process_file(path)

            self.assertEquals(mock_parse.called, True)
            tool.tmp_dir = temp
            calls = [mock.call(temp + os.sep + "0"), mock.call(temp + os.sep +
                                                               "1")]
            # pylint: disable=maybe-no-member
            os.mkdir.assert_has_calls(calls)
            extracts = [mock.call("bar.ear", "foo.war", temp + os.sep + "0"),
                        mock.call(temp + os.sep + "0" + os.sep + 'foo.war',
                                  'META-INF' + os.sep + 'lib' + os.sep +
                                  'baz.jar', temp + os.sep + "1"),
                        mock.call(temp + os.sep + "1" + os.sep + 'META-INF' +
                                  os.sep + 'lib' + os.sep + 'baz.jar',
                                  'baz.properties', target)
                        ]
            mock_extract.assert_has_calls(extracts)
            mock_return_file.assert_called_with(target + os.sep +
                                                'baz.properties')

            tool = None
            self.assertEquals(mock_clean_tmp.called, True)
            mock_parse.reset_mock()
            mock_clean_tmp.reset_mock()
            mock_extract.reset_mock()

        # pylint: disable=unused-argument,no-self-use
        @mock.patch.object(JarEarWarRar, 'return_file', return_value=True)
        @mock.patch.object(JarEarWarRar, 'extract_file', return_value=True)
        @mock.patch.object(JarEarWarRar, 'clean_tmp_dir', return_value=True)
        @mock.patch.object(JarEarWarRar, 'parse_java_path',
                           return_value=['baz.jar', 'baz.properties'])
        def test_process_file_2_files(self, mock_parse, mock_clean_tmp,
                                      mock_extract, mock_return_file):
            """Testing file processing with exception of single file"""
            # Special case of two elements
            path = 'baz.jar' + os.sep + 'baz.properties'
            temp = '/dev/shm/tempdir'
            target = temp+'/0'
            dest_dir = '/foo'
            shutil.move = mock.MagicMock(return_value=True)
            os.mkdir = mock.MagicMock(return_value=True)
            os.access = mock.MagicMock(return_value=True)
            tool = JarEarWarRar()
            tool.set_temp_dir(temp)
            tool.set_destination_dir(dest_dir)

            tool.process_file(path)
            extracts = [mock.call("baz.jar", "baz.properties", target)]
            mock_extract.assert_has_calls(extracts)
            mock_return_file.assert_called_with(target + os.sep +
                                                'baz.properties')
            tool = None

        @mock.patch.object(JarEarWarRar, 'set_destination_dir',
                           return_value=True)
        @mock.patch.object(JarEarWarRar, 'set_temp_dir', return_value=True)
        @mock.patch.object(JarEarWarRar, 'process_file', return_value=True)
        def test_main(self, mock_process, mock_set_temp, mock_dest_dir):
            """Testing console entrypoint and setting parameters"""
            # Test main with normal run
            with mock.patch.object(sys, 'argv', ['app.py',
                                   'foo.jar/foo.properties']):
                main()
                self.assertEquals(mock_set_temp.called, True)
                self.assertEquals(mock_dest_dir.called, True)
                self.assertEquals(mock_process.called, True)

        @mock.patch.object(JarEarWarRar, 'set_destination_dir',
                           return_value=True)
        @mock.patch.object(JarEarWarRar, 'set_temp_dir', return_value=True)
        @mock.patch.object(JarEarWarRar, 'process_file',
                           side_effect=IOError('foo'))
        def test_main_error(self, mock_process, mock_set_temp, mock_dest_dir):
            """Testing console entrypoint error propagation"""
            # Test main with Error
            devnull = open(os.devnull, 'w')
            with mock.patch('sys.stdout', devnull):
                with mock.patch('sys.stderr', devnull):
                    with mock.patch.object(sys, 'argv', ['app.py',
                                           'foo.jar/foo.properties']):
                        self.assertRaises(IOError, main)

    suite = unittest.TestLoader().loadTestsFromTestCase(ToolTestCases)
    unittest.TextTestRunner(verbosity=2).run(suite)


#
# Initial entry point.
#
def main():
    """docstring for Method"""
    # Hidden argument, --test launches internal testing sequence
    # for development purpose only, use at your own risk,
    # right?
    #
    # Hint: It might require some extra libs, which are imported on top of
    # test()
    if len(sys.argv) is 2 and sys.argv[1] == "--test":
        test()
        exit(0)

    parser = argparse.ArgumentParser(description='Tool to manage Java archive \
                                     types (jar, rar, ear, war). \
                                     Copyright (C) 2014  Harri Savolainen. \
                                     This program comes with ABSOLUTELY NO \
                                     WARRANTY; This is free software, and you \
                                     are welcome to redistribute it under \
                                     certain conditions. See GPL3v licence \
                                     for more information.')
    parser.add_argument('path', metavar='java_pgk_paths', help="Archive path \
                        with file appended (" + os.sep + "example.jar" +
                        os.sep + "file.class)")
    parser.add_argument('--destdir', default=None, help="Target directory to \
                        extract the file (defaults to current working dir \
                        [.])")
    parser.add_argument('--tempdir', default=None, help="Temporary directory \
                        to use (defaults to system temp or /dev/shm \
                        if available)")

    args = parser.parse_args()

    try:
        tool = JarEarWarRar()
        tool.set_destination_dir(args.destdir)
        tool.set_temp_dir(args.tempdir)
        tool.process_file(args.path)
    except:
        print "Error occured! Please see the messages."
        raise

if __name__ == '__main__':
    main()
