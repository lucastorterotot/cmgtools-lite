from PhysicsTools.Heppy.analyzers.core.TreeAnalyzerNumpy import TreeAnalyzerNumpy


class NtupleProducer(TreeAnalyzerNumpy):
        
    def declareVariables(self, event):
        for block in self.cfg_ana.event_content: 
            for varname, var in block.iteritems():
                self.tree.var(varname, var.vtype, var.default, varname, var.storageType)

    def process(self, event):
	for block in self.cfg_ana.event_content: 
            data = block.data_source(event)
            for varname, var in block.iteritems():
                try:
                    self.tree.fill(varname, var.function(data))
                except OverflowError:
                    print 'value', var.function(data), "didn't fit in var", varname
                    continue
        self.tree.tree.Fill()
