import FWCore.ParameterSet.Config as cms 
from RecoEgamma.EgammaTools.patPhotonDRNCorrectionProducer_cfi import patPhotonDRNCorrectionProducer
print("Started patPhotonsDRN module") #Checking if it runs
patPhotonsDRN = patPhotonDRNCorrectionProducer.clone(
                            particleSource = 'selectedPatPhotons',
                            rhoName = 'fixedGridRhoFastjetAll',
                            Client = patPhotonDRNCorrectionProducer.Client.clone(
                              mode = 'Async',
                              allowedTries = 1,
                              modelName = 'photonObjectCombined',
                              modelConfigPath = 'RecoEgamma/EgammaPhotonProducers/data/models/photonObjectCombined/config.pbtxt',
                              timeout = 10
                            )
    )
import os
full_model_config_path = os.popen('edmFileInPath RecoEgamma/EgammaPhotonProducers/data/models/photonObjectCombined/config.pbtxt').read().strip()

print("Full Model Config Path:", full_model_config_path)

