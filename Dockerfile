FROM python:3.12.9-slim-bookworm

RUN apt-get update && \
	apt-get install -y \
		git \
		libdbus-1-3 \
		libfontconfig \
		libgl1 \
		libglib2.0-0 \
		libxcb-icccm4 \
		libxcb-image0 \
		libxcb-keysyms1 \
		libxcb-render-util0 \
		libxcb-shape0 \
		libxcb-xinerama0 \
		libxcb-xkb1 \
		libxkbcommon-x11-0

RUN pip install \
	aiocoap[oscore,prettyprint] \
	opencv-python-headless \
	paho-mqtt \
	pglive \
	# https://github.com/MPI-IS/mesh/issues/23#issuecomment-1675645820
	PyOpenGL==3.1.1a1 \
	pyqt5 \
	# Using a PR from a random person directly seems going a bit too far just
	# for adding a dark theme but the white bars of the default theme were
	# getting stuck in my monitor for some reason so I take the risk.
	git+https://github.com/woopelderly/PyQtDarkTheme.git@python3.12 \
	numpy \
	pyqtgraph \
	scipy
