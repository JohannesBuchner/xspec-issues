import xspec

# compute flux with only model:

model = xspec.Model('powerlaw')
xspec.AllModels.calcFlux("2.3 6.0")
print(model.flux)
# works OK
assert model.flux[0] > 0


# clean up

xspec.AllData.clear()
xspec.AllModels.clear()
try:
	# this will fail as expected: model does not exist anymore
	model.flux
	assert False
except Exception:
	pass

# second version:

# try again with fakeit to include response

model = xspec.Model('powerlaw')
ero_settings = xspec.FakeitSettings(
	arf='arf01_100nmAl_200nmPI_sdtq.fits',
	response='rmf01_sdtq.fits',
	exposure=10000,
	background='bkg1000000.fak',
	fileName='test.fak',
)
xspec.AllData.fakeit(1, settings=[ero_settings])
xspec.AllModels.calcFlux("2.3 6.0")
print(model.flux)
# we expect a model count rate > 0 as before, but this fails
assert model.flux[0] > 0

