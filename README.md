jewr
====

 Java archive manager tool.

     $ python jewr.py -h
     usage: jewr.py [-h] [--destdir DESTDIR] [--tempdir TEMPDIR] java_pgk_paths
     
     Tool to manage Java archive types (jar, rar, ear, war). Copyright (C) 2014
     Harri Savolainen. This program comes with ABSOLUTELY NO WARRANTY; This is free
     software, and you are welcome to redistribute it under certain conditions. See
     GPL3v licence for more information.
     
     positional arguments:
       java_pgk_paths     Archive path with file appended (/example.jar/file.class)
     
     optional arguments:
       -h, --help         show this help message and exit
       --destdir DESTDIR  Target directory to extract the file (defaults to current
                          working dir [.])
       --tempdir TEMPDIR  Temporary directory to use (defaults to system temp or
                          /dev/shm if available)
      
