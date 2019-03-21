from PhysicsTools.Heppy.analyzers.core.TreeAnalyzerNumpy import TreeAnalyzerNumpy


class NtupleProducer(TreeAnalyzerNumpy):
        
    def declareVariables(self, event):
        for block in self.cfg_ana.event_content: 
            for varname, var in block.iteritems():
                self.tree.var(varname, var.vtype, var.default, varname, var.storageType)

    def process(self, event):
        if hasattr(self.cfg_ana, 'skim_func') and not self.cfg_ana.skim_func(event):
            return False
	for block in self.cfg_ana.event_content: 
            data = block.data_source(event)
            for varname, var in block.iteritems():
                try:
                    self.tree.fill(varname, var.function(data))
                except OverflowError:
                    print 'value', var.function(data), "didn't fit in var", varname
                    continue
                except TypeError:
                    message = 'Variable {} took the type: {} \n instead of the intended type: {}'.format(
			    varname,
			    str(type(var.function(data))),
			    str(var)
		    )
                    raise TypeError(message)
        self.tree.tree.Fill()
