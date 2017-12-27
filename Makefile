CORE_FONTS=Ubuntu-Light Ubuntu-LightItalic \
					 Ubuntu-Regular Ubuntu-Italic \
					 Ubuntu-Medium Ubuntu-MediumItalic \
					 Ubuntu-Bold Ubuntu-BoldItalic
MONO_FONTS=UbuntuMono-Regular UbuntuMono-Italic \
					 UbuntuMono-Bold UbuntuMono-BoldItalic
CONDENSED_FONTS=UbuntuCondensed-Regular
ALL_FONTS=$(CORE_FONTS) $(MONO_FONTS) $(CONDENSED_FONTS)

SRC_DIR=source
BUILD_DIR=build
MASTER_DIR=master_ttf

TTF=$(ALL_FONTS:%=$(BUILD_DIR)/%.ttf)
VTT_TTF=$(ALL_FONTS:%=$(SRC_DIR)/%.ttf)


all: ttf

ttf: $(TTF)

vtt: $(VTT_TTF)

$(SRC_DIR)/%.ttf: $(SRC_DIR)/%.ufo $(SRC_DIR)/%.ufo/*.plist \
                  $(SRC_DIR)/%.ufo/features.fea \
                  $(SRC_DIR)/%.ufo/glyphs*/*.glif \
                  $(SRC_DIR)/%.ufo/glyphs*/contents.plist \
                  $(SRC_DIR)/%.ufo/data/com.github.fonttools.ttx/*.ttx \
                  $(SRC_DIR)/%.ufo/data/com.daltonmaag.vttLib.plist
	python tools/build.py $< $@

$(BUILD_DIR)/%.ttf: $(SRC_DIR)/%.ttf
	@mkdir -p $(BUILD_DIR)
	python -m vttLib compile --ship $< $@
	bash tools/update-hinted-metrics.sh $@
	python tools/postprocess-hdmx-zero_out_unif000.py $@
	python tools/postprocess-kern.py $@

clean:
	@rm -rf $(BUILD_DIR)
	@rm -f $(VTT_TTF)

update-requirements:
	@bash tools/update-requirements.sh
