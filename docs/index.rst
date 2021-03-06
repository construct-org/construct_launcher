==================
construct_launcher
==================

Application Launching plugin for Construct.


Configuration
=============

Create an `apps` section in your Project's config like...

.. code-block::

    apps:
        maya2017:
            host: 'maya'
            identifier: 'launch.maya2017'
            description: 'Launch Autodesk Maya2017'
            icon: './icons/maya.png'
            cmd:
                win:
                    path: C:/Program Files/Autodesk/Maya2017/bin/maya.exe
                    args: []
                linux:
                    path: /usr/autodesk/maya2017/bin/maya
                    args: []
                darwin:
                    path: /Applications/Autodesk/maya2017/bin/maya
                    args: []



Now when your construct context is set to the project a new action named `launch.maya2017` will be available.


Installation
============

.. code-block:: console

    $ pip install git+ssh://git@github.com/construct-org/construct_launcher.git


.. toctree::
   :maxdepth: 2

   self
   guide

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
