from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

import sys
import pprint

class InteractiveDebug(Analyzer):

    def process(self, event):
        if not len(event.electrons):
            return 
        for ele in event.electrons:
            self.test_ele(ele)
        if self.cfg_ana.verbose:
            import pdb; pdb.set_trace()

    def test_ele(self, ele):
        if self.cfg_ana.verbose:
            print ele

        ## access to area table

        # access table in the class
        httiso = ele.iso_htt()
        table = ele.__class__.EffectiveArea03
        del ele.__class__.EffectiveArea03
        ele.EffectiveArea03 = table
        # access table in the object
        assert(ele.iso_htt()==httiso)
        del ele.EffectiveArea03
        # provide table to method
        assert(ele.relIso(0.3, "EA", 
                          area_table = table,
                          all_charged=False) == httiso)
        ele.__class__.EffectiveArea03 = table

        ## check that relIso is compatible with absIso
        reliso = ele.relIso(0.3, "EA", 
                            area_table = table,
                            all_charged=False)
        absiso = ele.absIso(0.3, "EA", 
                            area_table = table,
                            all_charged=False)
        assert(absiso/ele.pt() == reliso)

        ## check abs iso arguments: 
        
        area_table = table
        dbeta_factor = 0.5
        all_charged = False 

        args = [0.3]
        all_kwargs = dict( area_table = table,
                           dbeta_factor = 0.5,
                           all_charged = False) 

        succeeds = [
            ['area_table'],
            ['dbeta_factor'],
            ]
        fails = [
            ['area_table', 'dbeta_factor'],
            ['dbeta_factor', 'area_table'],
            ]
        
        def test_arglist(args, kwarglist, success=True): 
            for kwargssel in kwarglist: 
                kwargs = dict([ (name, all_kwargs[name]) for name in kwargssel ])
                # always needed
                kwargs['all_charged'] = all_kwargs['all_charged']
                the_args = list(args)
                if kwargssel[0].startswith('area'):
                    the_args.append('EA')
                elif kwargssel[0].startswith('dbeta'): 
                    the_args.append('dbeta')
                else:
                    the_args.append('raw')
                if self.cfg_ana.verbose:
                    pprint.pprint(the_args)
                    pprint.pprint(kwargs)
                if success:
                    ele.absIso(*the_args, **kwargs)
                else: 
                    try: 
                        ele.absIso(*the_args, **kwargs)
                    except:
                        pass
                    else:
                        msg = 'no exception caught\n'
                        msg += pprint.pformat(the_args)
                        msg += pprint.pformat(kwargs)
                        raise ValueError(msg)

        test_arglist(args, succeeds, success=True)
        test_arglist(args, fails, success=False)
        
        if self.cfg_ana.verbose:
            print 'all tests ok'

    
