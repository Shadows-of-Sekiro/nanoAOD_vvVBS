import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class wvAnalysisProducer(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        #self.out.branch("EventMass",  "F");
        """process event, return True (go to next module) or False (fail, go to next event)"""
        #pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """nanoAOD skimming is done considering the final events selection
        for the vv semileptonic final state.

        For the vv semileptonic final state we should be either one or two
        tight leptons, either one Fat jet and two small radius jet or four
        small radius jets.

        Arguments:
            event {instance of event} -- instance of event

        Returns:
            boolean -- if the event passes skimming then it returns true and
                       go to the next module else returns false and go to
                       the next event.
        """
        photons = Collection(event, "Photon")
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        fatJets = Collection(event, "FatJet")
        keepIt = True
        eventElectrons = 0
        eventMuons = 0
        eventJets = 0
        eventFatJets = 0
        if (len(photons)>0): print "\n\n=====> photons size: ",len(photons),type(photons)
        print "Lengths: ",len(photons)," ",len(electrons)," ",len(muons)," ",len(jets)," ",len(fatJets)

        for lep in muons :
            if lep.tightId and lep.pt > 10 :
                eventMuons += 1
        for lep in electrons :
            if lep.cutBased >= 2 and lep.pt > 10 :
                eventElectrons += 1
        for jet in jets :
            if jet.pt > 20:
               eventJets += 1
        for fatjet in fatJets :
            if fatjet.pt > 20:
               eventFatJets += 1

        if not ( ((eventElectrons >= 1 or eventMuons >=1)) and ( (eventJets >= 2 and eventFatJets >= 1) or (eventJets >= 4 and eventFatJets == 0) )  ):
            keepIt = False

        return keepIt


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
wvAnalysisModule = lambda : wvAnalysisProducer() #(jetSelection= lambda j : j.pt > 30)

