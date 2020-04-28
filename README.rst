========================
Bug reports for pyxspec
========================

getflux.py
-------------

The model count rate is zero after fakeit, but not when using just a model.

run with::

	python3 getflux.py


twosourcemodel.py
------------------

This sets up two sources, one going through the response, one not (diagonal dummy response).
The two sources are assigned to the background spectrum and the source spectrum.

The bug arises when the background data group is assigned background sources and responses.
This somehow changes the response for the source data group.

run with::

	python3 twosourcemodel.py workaround  # gives no error

	python3 twosourcemodel.py  # gives error


Additional nitpicks:

* It is very cumbersome to set this (pretty common) scenario up. Is there a better way?

* Setting to a non-existing response file triggers a command line question that *cannot be aborted*.

Responses used
-----------------

The RMF/ARF/background are arbitrary. In this case, they are taken from

https://wiki.mpe.mpg.de/eRosita/erocalib_calibration
https://wiki.mpe.mpg.de/eRosita/ScienceRelatedStuff/Background

These correspond to pre-flight estimations of eROSITA. They are not the real performance!


