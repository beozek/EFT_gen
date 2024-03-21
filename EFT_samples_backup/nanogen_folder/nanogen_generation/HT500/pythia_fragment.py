import FWCore.ParameterSet.Config as cms

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    #  tarball path
    args = cms.vstring('/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/EFT_samples/scripts_plots_new_samples/input_files/CA/TT01j1lCA_HT500_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz'),
    # number of events
    nEvents = cms.untracked.uint32(1000000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            'JetMatching:setMad = off',
            'JetMatching:scheme = 1',
            'JetMatching:merge = on',
            'JetMatching:jetAlgorithm = 2', #jet algorithm to use for jet clustering, couldn't find in run card ??
            'JetMatching:etaJetMax = 5.', #maximum pseudorapidity for the jets
            'JetMatching:coneRadius = 1.', #radius parameter for the jet clustering algorithm, couldn't find in run card ??
            'JetMatching:slowJetPower = 1', #type of jet algorithm in the run card, anti-kT or kT. couldn't find in run card ??
            'JetMatching:qCut = 10.', #this is the actual merging scale. it used to be 30. xqcut = 10 in datacard
            'JetMatching:nQmatch = 5', #5 for 5-flavour scheme (matching of b-quarks), the number of light flavors. run card: 5 = maxjetflavor 
            'JetMatching:nJetMax = 1', #number of partons in born matrix element for highest multiplicity. couldn't find in run card ??
            'JetMatching:doShowerKt = off', #off for MLM matching, turn on for shower-kT matching
        ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
    )
)



