import sys
import xspec

model = xspec.Model('powerlaw')
ero_settings = xspec.FakeitSettings(
	arf='arf01_100nmAl_200nmPI_sdtq.fits',
	response='rmf01_sdtq.fits',
	exposure=10000,
	background='bkg1000000.fak',
	fileName='test.fak',
)
xspec.AllData.fakeit(1, settings=[ero_settings])

src = xspec.AllData(1)
ilo = 1
ihi = 1024
bkgfile = src.background.fileName
arf, rmf = src.multiresponse[0].arf, src.multiresponse[0].rmf
src.background = None

# copy response to source 2
src.multiresponse[1] = rmf
src.multiresponse[1].arf = arf

# make unit response for background model:
clo = 1
src.dummyrsp(lowE=ilo, highE=ihi, nBins=ihi - ilo, scaleType="lin", chanOffset=clo, chanWidth=1, sourceNum=1)

# check that response is as expected
assert src.multiresponse[0].rmf == 'dummy'
assert src.multiresponse[1].rmf == 'rmf01_sdtq.fits'


# set background:

xspec.AllData("2:2 " + bkgfile)
bkg = xspec.AllData(2)

if len(sys.argv) > 1 and sys.argv[1] == "workaround":
    # make two responses, because starting with number 2 does not work.
    bkg.dummyrsp(lowE=ilo, highE=ihi, nBins=ihi - ilo, scaleType="lin", chanOffset=clo, chanWidth=1, sourceNum=1)
    bkg.dummyrsp(lowE=ilo, highE=ihi, nBins=ihi - ilo, scaleType="lin", chanOffset=clo, chanWidth=1, sourceNum=2)
    # delete the first response
    bkg.multiresponse[0] = None

else:
    
    bkg.dummyrsp(lowE=ilo, highE=ihi, nBins=ihi - ilo, scaleType="lin", chanOffset=clo, chanWidth=1, sourceNum=2)


srcmod = xspec.Model("zbbody", sourceNum=1)
bkgmod = xspec.Model("powerlaw", modName="bkgmod", sourceNum=2)

xspec.AllModels.show()
xspec.AllData.show()

# expected responses for source and background data:
rmf_expected = [
    'rmf01_sdtq.fits',
    'dummy',
    None,
    'dummy',
    ]

# get actual responses:
try:
    bkg_rmf = bkg.multiresponse[0].rmf
except Exception:
    bkg_rmf = None

rmf_values = [src.multiresponse[0].rmf, 
    src.multiresponse[1].rmf,
    bkg_rmf,
    bkg.multiresponse[1].rmf]

assert rmf_values == rmf_expected, ("RMFs disagree! actual settings:", rmf_values, "expected:", rmf_expected)
