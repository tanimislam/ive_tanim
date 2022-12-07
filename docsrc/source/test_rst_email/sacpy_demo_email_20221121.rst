Hello World!

This is a test email where I demonstrate using |rst| to write out rich emails. I also use |inline_images| to move the figures from remote links to embedded within the HTML.

|rst| is another markup language, used to create HTML documents in a pretty structured way rather than going down to the low level HTML + CSS + JavaScript.

So here's some example stuff, inline math here, like :math:`5x + 4y^2 - 3z = 0`. Some math delimited into its own blocks like here,

.. math::

   \frac{\partial^2\phi}{\partial x^2} + \frac{\partial^2\phi}{\partial y^2} + \frac{\partial^2\phi}{\partial z^2} + \frac{\omega^2}{c^2}\phi = 0.

And some other crap, like putting in images inline into here.

.. list-table:: here's a table of two images
   :widths: auto

   * - |iwanttobelieve_uncropped_cropped_local|
     - |turn_cartoon_local|
   * - Here's the demonstration image of autoCropImage_.
     - Here's my philosophy on driving shown here_.

And here we have an animated GIF_ of the *latest* (as of ``5 DECEMBER 2022``) 7-day rolling average of COVID-19 cases and deaths in the CONUS_.

.. list-table:: table showing an animated GIF
   :widths: auto

   * - |covid19_7day_conus_LATEST_CLIPPED|
   * - ``5 DECEMBER 2022`` 7-day rolling average of COVID-19 cases and deaths in the CONUS_. We create this animated GIF_ using `convertImage movie <https://tanimislam.github.io/iv_tanim/core_functionality.html#convertimage-movie>`_. Produces something that is 4.0 MB in size.
	
Now here's some stupid code blocks, some Python code in fact that I have here.

.. code-block:: python

   def _create_image_base64( img_path ):
       assert( os.path.exists( img_path ) )
       with Image.open( img_path ) as img, BytesIO( ) as buffered:
	   img.save( buffered, format = img.format )
	   img_str = base64.b64encode( buffered.getvalue()).decode('utf8')
	   return img_str

And here is some other code, this time another code block, this time |rst|.

.. code-block:: restructuredtext

   .. |rst| replace:: `RestructuredText`_
   .. _`RestructuredText`: https://en.wikipedia.org/wiki/ReStructuredText

Hope this was useful!

Tanim

.. note::

   This is based off an older demonstration email I sent out to PyRVA_ on 2022-03-09 and to SacPy_ on 2022-04-07.
		
.. |rst| replace:: `RestructuredText`_
.. _`RestructuredText`: https://en.wikipedia.org/wiki/ReStructuredText

.. |inline_images| replace:: ``inline_images``

.. _autoCropImage: https://tanimislam.github.io/iv_tanim/core_functionality.html#autocropimage
.. _here: https://tanimislam.github.io/nprstuff/driving.html#my-philosopy-on-driving

.. |iwanttobelieve_uncropped_cropped| image:: https://tanimislam.github.io/iv_tanim/_images/cumulative_plot_emission_uncropped_cropped.png
   :width: 50%
   :align: middle

.. |turn_cartoon| image:: https://tanimislam.gitlab.io/blog/2020/09/driving/turn_cartoon.png
   :width: 100%
   :align: middle

.. |iwanttobelieve_uncropped_cropped_local| image:: iwanttobelieve_uncropped_cropped.png
   :width: 50%
   :align: middle

.. |turn_cartoon_local| image:: turn_cartoon.png
   :width: 100%
   :align: middle

.. |covid19_7day_conus_LATEST_CLIPPED| image:: covid19_7day_conus_LATEST_CLIPPED.gif
   :width: 100%
   :align: middle

.. _MP4: https://en.wikipedia.org/wiki/MPEG-4_Part_14

.. _`this blog page`: https://tanimislam.gitlab.io/blog/2020-year-in-review.html

.. _PyRVA: http://www.pyrva.org

.. _SacPy: http://sacpy.org

.. |quaker_mp4| raw:: html

   <video controls width="100%">
   <source src="https://tanimislam.sfo3.digitaloceanspaces.com/blog/2020/12/Quaker_2020_WTF.mp4">
   </video>

.. _CONUS: https://en.wikipedia.org/wiki/Contiguous_United_States
.. _GIF: https://en.wikipedia.org/wiki/GIF
