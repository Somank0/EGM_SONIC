import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")

process.load("RecoEgamma.ElectronIdentification.egmGsfElectronIDs_cfi")
process.load("RecoEgamma.ElectronIdentification.egmGsfElectronIDs_cff")
process.load("RecoEgamma.EgammaElectronProducers.gedGsfElectrons_cfi")  # Explicitly load gedGsfElectrons
process.load("RecoEgamma.EgammaElectronProducers.gedGsfElectronSequence_cff")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

options = VarParsing.VarParsing('standard')

options.register('inputFile',
        "~/",
        VarParsing.VarParsing.multiplicity.singleton,
        VarParsing.VarParsing.varType.string,
        "File containing a list of the EXACT location of the output file  (default = ~/)"
        )

options.register('outputPath',
        '/eos/user/s/sosaha/EGM_test_Sonic/CMSSW_13_3_3/src/Test/Electron_RefinedRecHit_NTuplizer/python/Skimmed',
        VarParsing.VarParsing.multiplicity.singleton,
        VarParsing.VarParsing.varType.string,
        "Path to save the output file"
        )
options.register('RegressionType',
                 'BDT',  # Default is BDT if not specified
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Specify the type of input: BDT or DRN")
options.parseArguments()
print(f"Input file name : {options.inputFile}")
print(f"Regression type: {options.RegressionType}")
print(f"Output file will be saved to: {options.outputPath}")

if options.RegressionType == 'BDT':
    output_directory = options.outputPath + '/BDT/'
elif options.RegressionType == 'DRN':
    output_directory = options.outputPath + '/DRN/'
else:
    raise ValueError("Invalid Regression Type. Must be either 'BDT' or 'DRN'.")

#infilename = str(options.inputFile).split('/')[-1]

process.source = cms.Source("PoolSource",
                                # replace 'myfile.root' with the source file you want to use
                                fileNames = cms.untracked.vstring(
                #'root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18RECO/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/270004/22C4E1FC-D896-2345-B4F5-05CAD89E343E.root'
                options.inputFile
                ),
                inputCommands=cms.untracked.vstring(
                #'drop recoTrackExtrasedmAssociation_muonReducedTrackExtras_*_*'
                'keep *'
                )
                            )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')

from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
dataFormat = DataFormat.AOD
switchOnVIDElectronIdProducer(process, dataFormat)


# define which IDs we want to produce
my_id_modules = ['RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Fall17_94X_V2_cff']


for idmod in my_id_modules:
        setupAllVIDIdsInModule(process, idmod, setupVIDElectronSelection)

process.nTuplelize = cms.EDAnalyzer('Electron_RefinedRecHit_NTuplizer',
        rhoFastJet = cms.InputTag("fixedGridRhoAll"),
        electrons = cms.InputTag("gedGsfElectrons"),
        genParticles = cms.InputTag("genParticles"),
        refinedCluster = cms.bool(False),
        isMC = cms.bool(True), 
        miniAODRun = cms.bool(False),
        #MVA Based Id
	    eleLooseIdMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V2-loose"),
        eleMediumIdMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V2-medium"),
        eleTightIdMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V2-tight")
        )


process.TFileService = cms.Service("TFileService",
     #fileName = cms.string("ElectronRecHits_ntuple.root"),
     fileName = cms.string(output_directory +"DYtoLL_file1_ntuple.root"),
     closeFileFast = cms.untracked.bool(True)
  )


process.p = cms.Path(process.egmGsfElectronIDSequence*process.nTuplelize)

