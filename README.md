> [!IMPORTANT]
> **Slashmad Fork Patch Block (updated 2026-02-20)**
>
> Scope:
> - This block documents **fork-specific changes** on branch `slashmad` in this `gramps` repo.
>
> Desktop media workflow patches:
> - **Auto-import to typed subfolders**: media selected from editors/galleries is copied into the configured media base path and organized under `persons`, `families`, `events`, `places`, `sources`, `citations`.
> - **Duplicate reuse prompt**: if an identical file is already present in the media tree, the user can reuse it instead of creating a duplicate.
> - **Copy/Move import prompt**: import flow now asks whether to copy (keep source) or move (relocate source) the selected file.
> - **Gallery browse button**: gallery tabs include a button next to `+` that opens the relevant category folder directly and allows linking already-managed files.
> - **Media view drag-and-drop hardening**: drag-and-drop in Media view imports into managed media paths (instead of leaving unmanaged external file references), with category routing support.
>
> UX and localization:
> - **Safer copy-first flow**: button order and default response are tuned for copy-first behavior.
> - **Swedish strings for new flows**: new media import/browse strings are translated in `po/sv.po` (with runtime fallback where needed).
> - **Source/Citation autocomplete**: added focus-only, lazy-loaded autocomplete for source editor fields (`author`, `publication info`, `abbreviation`, `title`) and citation `volume/page`, based on existing stored values, with `Esc` to dismiss suggestions in the active field.
> - **Call-name highlighting in person lists**: new Text preferences allow highlighting names that have a call name with **bold**, **underline**, or both.
>
> Filter and relationship improvements:
> - **New person source scope rules (person + linked events)**:
>   - `People with <count> sources (person + linked events)`
>   - `People with the <source> (person + linked events)`
>   - `People missing sources (person + linked events)`
> - **New relatedness rules with Home Person support**:
>   - `People related to <Person/Home Person>`
>   - `People NOT related to <Person/Home Person>`
> - **Not Related diagnostics**: the `Not Related` tool now shows `Component` and `Diagnostic` columns to explain disconnections in the relationship graph.
>
> Build/version policy in this fork:
> - Keep upstream app version as **`6.0.6`** (no local build identity suffix in runtime version string).
>
> Related fork work (separate repos):
> - `slashmad/addons-source`: Theme/Dark mode add-on improvements and GrampsWebSync local patching used in this environment.

[The Gramps Project](https://gramps-project.org)
===================
[![GitHub CI](https://github.com/gramps-project/gramps/actions/workflows/gramps-ci.yml/badge.svg?event=push&branch=maintenance/gramps60)](https://github.com/gramps-project/gramps/actions/workflows/gramps-ci.yml?query=branch%3Amaintenance/gramps60)
[![codecov.io](https://codecov.io/github/gramps-project/gramps/coverage.svg?branch=maintenance/gramps60)](https://app.codecov.io/gh/gramps-project/gramps/branch/maintenance/gramps60)
[![Translation status](https://hosted.weblate.org/widgets/gramps-project/-/gramps/svg-badge.svg)](https://hosted.weblate.org/engage/gramps-project)

We strive to produce a genealogy program that is both intuitive for hobbyists and feature-complete for professional genealogists.

Please read the [**COPYING**](https://github.com/gramps-project/gramps/blob/maintenance/gramps60/COPYING) file first.

Please read the [**INSTALL**](https://github.com/gramps-project/gramps/blob/maintenance/gramps60/INSTALL) file if you intend to build from source.

Requirements
============
The following packages **MUST** be installed in order for Gramps to work:

* [**Python**](https://www.python.org/) 3.9 or greater - The programming language used by Gramps.
* [**GTK**](http://www.gtk.org/) 3.24 or greater - A cross-platform widget toolkit for creating graphical user interfaces.
* [**pygobject**](https://wiki.gnome.org/Projects/PyGObject) 3.12 or greater - Python Bindings for GLib/GObject/GIO/GTK+

The following three packages with GObject Introspection bindings (the gi packages)

* [**cairo**](http://cairographics.org/) 1.14.0 or greater - a 2D graphics library with support for multiple output devices.
* [**Pycairo**](https://github.com/pygobject/pycairo) 1.13.3 or greater - GObject Introspection bindings for cairo.
* [**pango**](http://www.pango.org/) - a library for laying out and rendering of text, with an emphasis on internationalization.
* [**pangocairo**](http://www.pango.org/) - Allows you to use Pango with Cairo.
* [**librsvg2**](http://live.gnome.org/LibRsvg) - (SVG icon view) a library to render SVG files using cairo.
* [**orjson**](https://pypi.org/project/orjson/) - A fast JSON library for Python. Used to increase the performance of Gramps.

The following package is needed for full translation of the interface
to your language:

*   **language-pack-gnome-xx**

 Translation of GTK elements to your language, with
 xx your language code; e.g. for Dutch you need
 language-pack-gnome-nl. The translation of the
 Gramps strings is included with the Gramps source.


The following packages are **STRONGLY RECOMMENDED** to be installed:
--------------------------------------------------------------------
*  [**osmgpsmap**](https://nzjrs.github.io/osm-gps-map/)

 Used to show maps in the [Geography Category](https://gramps-project.org/wiki/index.php?title=Gramps_6.0_Wiki_Manual_-_Categories#Geography_Category).
 It may be osmgpsmap, osm-gps-map, or python-osmgpsmap,
 but the Python bindings for this must also be present, so gir1.2-osmgpsmap-1.0.
 Without this the GeoView will not be active.

* [**Graphviz**](http://www.graphviz.org)

  Enable creation of graphs using Graphviz engine.
  Without this, three reports cannot be run.
  The package name is usually graphviz or python3-pygraphviz.

* [**PyICU**](http://pyicu.osafoundation.org/)

 Improves localised sorting in Gramps. In particular, this
 applies to sorting in the various views and in the
 Narrative Web output. It is particularly helpful for
 non-Latin characters, for non-English locales and on MS
 Windows and Mac OS X platforms. If it is not available,
 sorting is done through built-in libraries. PyICU is
 fairly widely available through the package managers of
 distributions.
 (These are Python bindings for the ICU package
 https://pypi.python.org/pypi/PyICU/).

* [**Ghostscript**](https://www.ghostscript.com)

  Used by Graphviz reports to help create PDF files.

* [**python-imagesize**](https://pypi.org/project/imagesize/)

 Provides better image processing performance. If this module is not available,
 we continue to use Gdk. This provides a real improvement when we need to
 process many big images.


The following packages are optional:
------------------------------------
* [**bsddb3**](https://pypi.python.org/pypi/bsddb3/)

Python bindings for Oracle Berkeley database. Only needed to upgrade older Gramps databases.

* **gspell**

 Enable spell checking in the notes.

* [**rcs**](https://www.gnu.org/software/rcs/)

 The GNU Revision Control System (RCS) can be used to
 [archive a family tree](https://gramps-project.org/wiki/index.php?title=Gramps_6.0_Wiki_Manual_-_Manage_Family_Trees#Archiving_a_Family_Tree).
 Multiple revisions of your family trees can be managed.
 Only rcs is needed, NO python bindings are required.

* [**Pillow**](https://python-pillow.org)

 The friendly Python Image Library fork is needed to crop
 images and also to convert non-JPG images to
 JPG so as to include them in LaTeX output.
 The package name is usually python-pillow or python3-pillow.

* [**gexiv2**](https://wiki.gnome.org/Projects/gexiv2) 0.5 or greater

 Enables Gramps to manage Exif metadata embedded in your
 media.

* [**ttf-freefont**](https://savannah.gnu.org/projects/freefont/)

 Provides genealogical symbols and more fonts for reports

* **geocode-glib**

 A library use to associate a geographical position (latitude, longitude)
 to a place name. This is used if you already have osmgpsmap installed.
 If installed, when you add or link a place from the map, you have a red line
 at the end of the table for selection.
 The package name is usually gir1.2-geocodeglib-1.0 or geocode-glib.

* [**fontconfig**](https://www.freedesktop.org/wiki/Software/fontconfig/)

 Python bindings of fontconfig are required for displaying
 genealogical symbols

* [**pycountry**](https://pypi.org/project/pycountry/)

 Used to validate ISO language codes.


Optional packages required by Third-party Addons
------------------------------------------------

**[Third-party Addons](https://gramps-project.org/wiki/index.php?title=Third-party_Plugins) are written by users and developers and unless stated are not officially part of Gramps.**

Prerequistes required for the following Addons to work:

* [**Family Sheet**]( https://gramps-project.org/wiki/index.php?title=Family_Sheet ) - Requires: Pillow
* [**Graph View**]( https://gramps-project.org/wiki/index.php?title=Graph_View ) - Requires: PyGoocanvas and Goocanvas (python-pygoocanvas, gir1.2-goocanvas-2.0).
* [**Network Chart**]( https://gramps-project.org/wiki/index.php?title=NetworkChart ) - Requires: networkx and pygraphviz
* [**PedigreeChart**]( https://gramps-project.org/wiki/index.php?title=PedigreeChart ) - Can optionally use - numpy if installed


No longer needed:
-----------------
* Since Gramps 5.2:
   **xdg-utils**

* Since Gramps 4.2:
   **gir-webkit**

* Since Gramps 4.0:
   **pygoocanvas, pygtk, pyexiv2**

* Since Gramps 3.3:
   **python-enchant Enchant**

* Since Gramps 3.2:
   **python glade bindings**

* Since Gramps 3.1:
   **yelp** - Gnome help browser. No offline help is shipped see Gramps website for User manual


Documentation
-------------

The [User Manual](https://www.gramps-project.org/wiki/index.php?title=User_manual) is maintained on the Gramps website.


Bug Tracker
-------------

Use the Gramps [Bug Tracker](https://gramps-project.org/bugs/my_view_page.php) to report bugs and suggest new features.


Translation
-------------

Gramps uses [Hosted Weblate](https://hosted.weblate.org/engage/gramps-project) for its translations.
