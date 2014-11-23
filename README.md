JEWR
====

A tool to **"chew"** java archives, **JEWR** (pronounced as '*Chewer*'). JEWR is short for the supported java archive types: JAR, EAR, WAR and RAR.

PREFACE
------
Simplifies post-management of java archives. Typical use-cases include the listing of files inside deep hierarchical package structure, extracting the configuration files (or any other files) from the archives and replacing the existing files inside package structure. Supersedes sequential jar -xf, jar -uf and jar -tf sequences. Manages creation and deletion of temporary directories and automates the other tasks to extract and repack files within java archives and their sub-archives without depth limitations.

FEATURES
--------
- Manages the archives inside the archives of any depth
- Extracting a single file from the package structure
- Replacing a single file in any package structure
- Listing the files in the any archive structure
- A simple detection of the jar command location
- Auto-setting of the temporary directory

PRE-REQUIREMENTS
----------------
- Requires any JDK "jar" command for package update operation with command line switches (-u) and (-f)
- Python 2.6+
- python-argparse (included in Python 2.7+)

USAGE
-----
    $ python jewr.py -h
    usage: jewr.py [-h] [-d DESTDIR] [-t TEMPDIR] [-j JARPATH] [-r REPLACE] [-l]
                   [-v]
                   java_pgk_paths

    Tool to manage Java archive types (jar, rar, ear, war). Copyright (C) 2014
    Harri Savolainen. This program comes with ABSOLUTELY NO WARRANTY; This is free
    software, and you are welcome to redistribute it under certain conditions. See
    GPL3v licence for more information.

    positional arguments:
      java_pgk_paths        Archive path including filenames as single path, i.e.
                            example.ear/example.war/lib/example.jar/META-
                            INF/MANIFEST.MF or when listing files, part of the
                            path i.e. example.ear/example.war/lib/example.jar
                            /META-INF

    optional arguments:
      -h, --help            show this help message and exit
      -d DESTDIR, --destdir DESTDIR
                            Target director to extract the file (defaults to
                            current working dir [.])
      -t TEMPDIR, --tempdir TEMPDIR
                            Temporary directory to use (defaults to system temp or
                            /dev/shm if available)
      -j JARPATH, --jarpath JARPATH
                            Path to jar command, which is required for repacking
                            archives. Defaults to /usr/bin/jar. Honors also
                            JEWR_JAVA_HOME or secondarily JAVA_HOME environment
                            variables which also can used to set the path.
      -r REPLACE, --replace REPLACE
                            File name with path when replacing the file inside the
                            archieve structure
      -l, --list            List path files
      -v, --verbose         Add verbosity

USAGE EXAMPLES
--------------
Listing files of sample.war:

    $ python jewr.py sample.war -l

    META-INF/
    META-INF/MANIFEST.MF
    META-INF/lib/
    META-INF/lib/servlet.jar
    WEB-INF/
    WEB-INF/classes/
    ...

Listing files inside servlet.jar in the depths of sample.war:

    $ python jewr.py sample.war/META-INF/lib/servlet.jar -l

    META-INF/MANIFEST.MF
    META-INF/
    META-INF/LICENSE
    META-INF/NOTICE
    META-INF/maven/
    META-INF/maven/org.apache.tomcat/
    META-INF/maven/org.apache.tomcat/tomcat-servlet-api/
    META-INF/maven/org.apache.tomcat/tomcat-servlet-api/pom.properties
    javax/
    javax/servlet/
    javax/servlet/AsyncContext.class
    ...

Filtering file list to "javax"-package of previous example:

    $ python jewr.py sample.war/META-INF/lib/servlet.jar/javax -l

    javax/
    javax/servlet/
    javax/servlet/AsyncContext.class
    ...

Any number of letters filters the file list:

    $ python jewr.py sample.war/META-INF/lib/servlet.jar/M -l

    META-INF/MANIFEST.MF
    META-INF/
    META-INF/LICENSE
    ...

Extracting pom.properties file from the depths of sample.war:

    $ python jewr.py sample.war/META-INF/lib/servlet.jar/META-INF/maven/org.apache.tomcat/tomcat-servlet-api/pom.properties

The pom.properties appears in current working dir. Destination can be changed with -d  switch.

Replacing file with another to depths of sample.war:

    $ python jewr.py sample.war/META-INF/lib/servlet.jar/META-INF/maven/org.apache.tomcat/tomcat-servlet-api/pom.properties -r newpom.properties

The file in the package will remain with the same name regardless the name of the replacing file.

Setting Jar command path (lookup order):

- Using switch (-j [path])
- JEWR_JAVA_HOME environment variable
- JAVA_HOME environment variable
- If none of above is found, defaults to /usr/bin/jar (this will most likely fail on quite many platforms)

Setting Temporary directory (lookup order):

- Temporary dir can be set with -t [path]
- /dev/shm is used if found (for performance)
- Falls back on platform default temp dir determined by Python

Making JEWR executable (on linux/unix systems):

- Add hashbang e.g (#!/usr/bin/env python or #!/usr/bin/env python3 on the first line)
- Make the file executable (chmod a+x jewr.py)

DEVELOPER INFO
--------------
- Verified passing PEP8
- Verified passing Pylint (with some disabled warnings)
- Includes unit test suite, can be launched with hidden switch '--test'
- Single test can be run with appended ':' followed by test name (eg --test:test_name)
- Test suite requires some extra dependencies. See source code comments for details.

LICENCE AND AUTHOR
------------------
**Author:** Harri Savolainen 2014

**License:** GPLv3

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




