class Rule:
    def __init__(self, conditions, conclusions):
        if not isinstance(conditions, set) or not isinstance(conclusions, set):
            raise ValueError("Conditions and conclusions must be sets.")
        self.conditions = conditions
        self.conclusions = conclusions

    def applies(self, beliefs):
        return self.conditions.issubset(beliefs)


class Default:
    def __init__(self, conditions, conclusions):
        if not isinstance(conditions, set) or not isinstance(conclusions, set):
            raise ValueError("Conditions and conclusions must be sets.")
        self.conditions = conditions
        self.conclusions = conclusions

    def applies(self, beliefs):
        return self.conditions.isdisjoint(beliefs)


class DefaultLogic:
    def __init__(self):
        self.rules = []
        self.defaults = []

    def add_rule(self, rule):
        """
        Add a rule to the set of rules.
        """
        if not isinstance(rule, Rule):
            raise ValueError("Rule must be an instance of Rule.")
        self.rules.append(rule)

    def add_default(self, default):
        """
        Add a default to the set of defaults.
        """
        if not isinstance(default, Default):
            raise ValueError("Default must be an instance of Default.")
        self.defaults.append(default)

    def evaluate(self, query):
        """
        Evaluate a query using Default Logic.
        """
        beliefs = set()
        new_beliefs = set()

        while True:
            new_beliefs.clear()

            # Apply rules to expand beliefs
            for rule in self.rules:
                if rule.applies(beliefs):
                    new_beliefs.update(rule.conclusions)

            # Apply defaults to fill gaps
            for default in self.defaults:
                if default.applies(beliefs):
                    new_beliefs.update(default.conclusions)

            if new_beliefs.issubset(beliefs):
                break

            beliefs.update(new_beliefs)

        return query in beliefs


if __name__ == "__main__":
    # Create a DefaultLogic instance
    dl = DefaultLogic()

    # Define rules and defaults using Rule and Default classes
    rule1 = Rule({"A", "B"}, {"C"})
    rule2 = Rule({"D"}, {"E"})
    default1 = Default({"F"}, {"G"})
    default2 = Default({"H"}, {"I"})

    dl.add_rule(rule1)
    dl.add_rule(rule2)
    dl.add_default(default1)
    dl.add_default(default2)

    # Query the Default Logic system
    query = "C"
    result = dl.evaluate(query)

    # Print the result
    if result:
        print(f"The query '{query}' is concluded.")
    else:
        print(f"The query '{query}' is not concluded.")

