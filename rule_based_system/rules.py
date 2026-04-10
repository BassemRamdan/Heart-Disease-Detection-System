import collections.abc
import collections
collections.Mapping = collections.abc.Mapping
collections.MutableMapping = collections.abc.MutableMapping
collections.Iterable = collections.abc.Iterable
collections.MutableSet = collections.abc.MutableSet
collections.Callable = collections.abc.Callable

from experta import *

class Patient(Fact):
    """Information about the patient."""
    pass

class HeartDiseaseEngine(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.matched_rules = []
        self.high_risk = False
        self.moderate_risk = False
        self.low_risk = False

    def _flag(self, level: str, message: str) -> None:
        self.matched_rules.append(message)
        if level == "High":
            self.high_risk = True
        elif level == "Moderate":
            self.moderate_risk = True
        elif level == "Low":
            self.low_risk = True

    @Rule(AS.p << Patient(chol=MATCH.c, age=MATCH.a), TEST(lambda p, c, a: c > 240 and a > 50))
    def rule_1(self, p, c, a):
        self._flag("High", "High cholesterol (>240) with age >50")

    @Rule(AS.p << Patient(trestbps=MATCH.t, exang=MATCH.e), TEST(lambda p, t, e: t > 140 and e == 1))
    def rule_2(self, p, t, e):
        self._flag("High", "High BP (>140) with exercise-induced angina")

    @Rule(AS.p << Patient(thalach=MATCH.th, exang=MATCH.ex, age=MATCH.ag), 
          TEST(lambda p, th, ex, ag: th > 150 and ex == 0 and ag < 55))
    def rule_3(self, p, th, ex, ag):
        self._flag("Low", "Good exercise capacity + no angina + young age")

    @Rule(AS.p << Patient(chol=MATCH.c, trestbps=MATCH.t, fbs=MATCH.f), 
          TEST(lambda p, c, t, f: c > 200 and t > 130 and f == 1))
    def rule_4(self, p, c, t, f):
        self._flag("High", "Multiple risks: High cholesterol + BP + fasting blood sugar")

    @Rule(AS.p << Patient(cp=MATCH.c, oldpeak=MATCH.o), TEST(lambda p, c, o: c >= 2 and o > 1.5))
    def rule_5(self, p, c, o):
        self._flag("High", "Significant chest pain with ST depression >1.5")

    @Rule(AS.p << Patient(ca=MATCH.c), TEST(lambda p, c: c >= 2))
    def rule_6(self, p, c):
        self._flag("High", "2+ major vessels colored by fluoroscopy")

    @Rule(AS.p << Patient(thal=P(lambda x: x in [1, 2])))
    def rule_7(self, p):
        self._flag("Moderate", "Thalassemia defect detected")

    @Rule(AS.p << Patient(age=MATCH.a, chol=MATCH.c, trestbps=MATCH.t, fbs=MATCH.f), 
          TEST(lambda p, a, c, t, f: a < 45 and c < 200 and t < 120 and f == 0))
    def rule_8(self, p, a, c, t, f):
        self._flag("Low", "Young age with all normal health indicators")

    @Rule(AS.p << Patient(restecg=MATCH.r, exang=MATCH.e), TEST(lambda p, r, e: r == 0 and e == 0))
    def rule_9(self, p, r, e):
        self._flag("Low", "Normal ECG with no exercise angina")

    @Rule(AS.p << Patient(slope=MATCH.s, oldpeak=MATCH.o), TEST(lambda p, s, o: s == 2 and o > 2.0))
    def rule_10(self, p, s, o):
        self._flag("High", "Flat slope with high ST depression (>2.0)")

    @Rule(AS.p << Patient(sex=MATCH.s, cp=MATCH.c), TEST(lambda p, s, c: s == 0 and c >= 1))
    def rule_11(self, p, s, c):
        self._flag("Moderate", "Female with chest pain symptoms")

    @Rule(AS.p << Patient(sex=MATCH.s, age=MATCH.a, exang=MATCH.e), 
          TEST(lambda p, s, a, e: s == 1 and a > 55 and e == 1))
    def rule_12(self, p, s, a, e):
        self._flag("High", "Male >55 years with exercise-induced angina")

    def get_result(self) -> dict:
        if self.high_risk:
            final_risk = "High"
        elif self.moderate_risk:
            final_risk = "Moderate"
        elif self.low_risk:
            final_risk = "Low"
        else:
            final_risk = "Moderate"
            self.matched_rules.append("General assessment based on available data")

        return {
            "risk_level": final_risk,
            "matched_rules": self.matched_rules,
            "num_rules_matched": len(self.matched_rules),
        }

def assess_patient(patient_data: dict) -> dict:
    engine = HeartDiseaseEngine()
    engine.reset()
    
    clean_data = {k: v for k, v in patient_data.items() if v is not None}
    
    # Fill defaults to prevent EXPERTA matching errors if a key is missing
    defaults = {
        'age': 100, 'sex': -1, 'cp': 0, 'trestbps': 0, 'chol': 0,
        'fbs': -1, 'restecg': -1, 'thalach': 0, 'exang': -1,
        'oldpeak': 0.0, 'slope': -1, 'ca': 0, 'thal': -1
    }
    for k, v in defaults.items():
        if k not in clean_data:
            clean_data[k] = v
            
    engine.declare(Patient(**clean_data))
    engine.run()
    return engine.get_result()

if __name__ == "__main__":
    test_patient = {
        "age": 65, "sex": 1, "cp": 3, "trestbps": 150, "chol": 260,
        "fbs": 1, "restecg": 1, "thalach": 120, "exang": 1,
        "oldpeak": 2.5, "slope": 2, "ca": 3, "thal": 2,
    }
    print(assess_patient(test_patient))
