import read, copy
from util import *
from logical_classes import *

verbose = 0

class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
        self.ie = InferenceEngine()

    def __repr__(self):
        return 'KnowledgeBase({!r}, {!r})'.format(self.facts, self.rules)

    def __str__(self):
        string = "Knowledge Base: \n"
        string += "\n".join((str(fact) for fact in self.facts)) + "\n"
        string += "\n".join((str(rule) for rule in self.rules))
        return string

    def _get_fact(self, fact):
        """INTERNAL USE ONLY
        Get the fact in the KB that is the same as the fact argument

        Args:
            fact (Fact): Fact we're searching for

        Returns:
            Fact: matching fact
        """
        for kbfact in self.facts:
            if fact == kbfact:
                return kbfact

    def _get_rule(self, rule):
        """INTERNAL USE ONLY
        Get the rule in the KB that is the same as the rule argument

        Args:
            rule (Rule): Rule we're searching for

        Returns:
            Rule: matching rule
        """
        for kbrule in self.rules:
            if rule == kbrule:
                return kbrule

    def kb_add(self, fact_rule):
        """Add a fact or rule to the KB
        Args:
            fact_rule (Fact|Rule) - the fact or rule to be added
        Returns:
            None
        """
        printv("Adding {!r}", 1, verbose, [fact_rule])
        if isinstance(fact_rule, Fact):
            if fact_rule not in self.facts:
                self.facts.append(fact_rule)
                for rule in self.rules:
                    self.ie.fc_infer(fact_rule, rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.facts.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.facts[ind].supported_by.append(f)
                else:
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = True
        elif isinstance(fact_rule, Rule):
            if fact_rule not in self.rules:
                self.rules.append(fact_rule)
                for fact in self.facts:
                    self.ie.fc_infer(fact, fact_rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.rules.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.rules[ind].supported_by.append(f)
                else:
                    ind = self.rules.index(fact_rule)
                    self.rules[ind].asserted = True

    def kb_assert(self, fact_rule):
        """Assert a fact or rule into the KB

        Args:
            fact_rule (Fact or Rule): Fact or Rule we're asserting
        """
        printv("Asserting {!r}", 0, verbose, [fact_rule])
        self.kb_add(fact_rule)

    def kb_ask(self, fact):
        """Ask if a fact is in the KB

        Args:
            fact (Fact) - Statement to be asked (will be converted into a Fact)

        Returns:
            listof Bindings|False - list of Bindings if result found, False otherwise
        """
        print("Asking {!r}".format(fact))
        if factq(fact):
            f = Fact(fact.statement)
            bindings_lst = ListOfBindings()
            # ask matched facts
            for fact in self.facts:
                binding = match(f.statement, fact.statement)
                if binding:
                    bindings_lst.add_bindings(binding, [fact])

            return bindings_lst if bindings_lst.list_of_bindings else []

        else:
            print("Invalid ask:", fact.statement)
            return []

    def remove_helper(self, fact):

        # helper function to aid in kb_retract



        if isinstance(fact, Fact):   
            if fact in self.facts:  
  
                fact = self._get_fact(fact)  
                fac_sup = fact.supported_by  

                if len(fac_sup) != 0:  
  
                    fact.asserted = False   
   
                else:
                    if fac_sup != False:
                        for i in fact.supports_facts: 

                            sportsf = self._get_fact(i)  
                            sportsf_sup = sportsf.supported_by  

                            for j in sportsf_sup:        
                                if j[0] == fact:  

                                    sportsf_sup.remove(j)   

                            self.remove_helper(sportsf)  
  
                        for i in fact.supports_rules:   

                            sportsr = self._get_rule(i)  
                            sportsr_sup = sportsr.supported_by    

                            for j in sportsr_sup:     
                                if j[0] == fact:  
                                    sportsr_sup.remove(j)    

                            self.remove_helper(sportsr)   

                        self.facts.remove(fact)   

        elif isinstance(fact, Rule):    
            if fact in self.rules:       

                rule = self._get_rule(fact)      

                if (len(rule.supported_by) == 0):      
                    
                    for i in rule.supports_rules:   
                        if (not rule.asserted):      

                            sportsr = self._get_rule(i)     
                            sportsr_sup = sportsr.supported_by     

                            for j in sportsr_sup:      
                                if j[1] == rule:     

                                    sportsr_sup.remove(j)      

                            self.remove_helper(sportsr)    

                    self.rules.remove(rule)    

                    for i in rule.supports_facts:  
                        if (not rule.asserted):   
  
                            sportsf = self._get_fact(i)   
                            sportsf_sup = sportsf.supported_by   
  
                            for j in sportsf_sup: 
                                if j[1] == rule:    

                                    sportsf_sup.remove(j)  
 
                            self.remove_helper(sportsf) 


    def kb_retract(self, fact):
        """Retract a fact from the KB
        Args:
            fact (Fact) - Fact to be retracted
        Returns:
            None
        """
        printv("Retracting {!r}", 0, verbose, [fact])
        ####################################################
        # Student code goes here
        if isinstance(fact, Fact):
            self.remove_helper(fact) 








        

class InferenceEngine(object):
    def fc_infer(self, fact, rule, kb):
        """Forward-chaining to infer new facts and rules
        Args:
            fact (Fact) - A fact from the KnowledgeBase
            rule (Rule) - A rule from the KnowledgeBase
            kb (KnowledgeBase) - A KnowledgeBase
        Returns:
            Nothing            
        """
        printv('Attempting to infer from {!r} and {!r} => {!r}', 1, verbose,
            [fact.statement, rule.lhs, rule.rhs])
        ####################################################
        # Student code goes here
        
        mach = match(fact.statement, rule.lhs[0])
        lenth = len(rule.lhs)
        support = [(fact,rule)]

        if match(fact.statement, rule.lhs[0]) != False:

            if lenth==1:

                if isinstance(rule,Rule):

                     if isinstance(fact,Fact):

                        insta = instantiate(rule.rhs, mach)
                        infact = Fact(insta, support)

                        fact.supports_facts.append(infact)
                        rule.supports_facts.append(infact)

                        kb.kb_add(infact)

            else:

                if isinstance(rule,Rule):

                     if isinstance(fact,Fact):

                        inferred_lhs = []
                        leth = len(rule.lhs)

                        for i in rule.lhs[1:leth]:

                            inbind = instantiate(i, mach)
                            inferred_lhs.append(inbind)

                        inferred_rhs = instantiate(rule.rhs, mach)
                        inferred_rule = Rule([inferred_lhs, inferred_rhs], support)
                        fact.supports_rules.append(inferred_rule)
                        rule.supports_rules.append(inferred_rule)
                        kb.kb_add(inferred_rule)







