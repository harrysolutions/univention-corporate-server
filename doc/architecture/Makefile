# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: livehtml
livehtml:
	sphinx-autobuild "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: check
check::
	$(MAKE) linkcheck
	$(MAKE) spelling

.PHONY: install
install::
ifdef DESTDIR
	$(MAKE) html BUILDDIR="$(DESTDIR)"
	$(MAKE) latexpdf BUILDDIR="$(DESTDIR)"
	cp "$(DESTDIR)"/latex/ucs-architecture.pdf "$(DESTDIR)"/html/
else
	@echo "No DESTDIR environment variable defined. Skip."
endif

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
