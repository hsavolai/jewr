jewr
====

"Jar-Eer-War-Rar", the java archive manager tool.

Requires jar command in package update

               $ python jewr.py -h
               usage: jewr.py [-h] [--destdir DESTDIR] [--tempdir TEMPDIR]
                              [--jarpath JARPATH] [--replace REPLACE]
                              java_pgk_paths
               
               Tool to manage Java archive types (jar, rar, ear, war). Copyright (C) 2014
               Harri Savolainen. This program comes with ABSOLUTELY NO WARRANTY; This is
               free software, and you are welcome to redistribute it under certain conditions.
               See GPL3v licence for more information.
               
               positional arguments:
                 java_pgk_paths     Archive path including filename, i.e. 
                 					 example.jar/META-INF/file.class)
               
               optional arguments:
                 -h, --help         show this help message and exit
                 --destdir DESTDIR  Target directory to extract the file (defaults to current
                                    working dir [.])
                 --tempdir TEMPDIR  Temporary directory to use (defaults to system temp or
                                    /dev/shm if available)
                 --jarpath JARPATH  Path to jar command, which is required for repacking
                                    archives. Defaults to /usr/bin/jar. Honors also
                                    JEWR_JAVA_HOME or secondarily JAVA_HOME environment
                                    variables which also can used to set the path.
                 --replace REPLACE  File name with path when replacing the file inside the
                                    archieve structure
