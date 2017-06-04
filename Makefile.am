SUBDIRS = src

EXTRA_DIST = debian README.md

README: README.md
	fgrep -v "[Build Status]" $< | \
	markdown | \
	html2text -style pretty -nobs | \
	sed -e 's:&gt;:>:g' > $@

