import sys
sys.path.append('..')

from RaAuto.RaAuto import *

class ImgsEnum:
    def __init__(self, imagesPath):
        self.ArbetsflodeLabel = os.path.join(imagesPath, "ArbetsflodeLabel.png")
        self.StangButtonText = os.path.join(imagesPath, "Vaccine", "StangButtonText.png")
        self.NyDiagnosTab = os.path.join(imagesPath, "Vaccine", "NyDiagnosTab.png")
        self.KshDropdownChoice = os.path.join(imagesPath, "KshDropdownChoice.png")
        self.KshDropdownChoice2 = os.path.join(imagesPath, "KshDropdownChoice2.png")
        self.Icd10DropdownChoice = os.path.join(imagesPath, "icd10DropdownChoice.png")
        self.IcdSearchInputField = os.path.join(imagesPath, "icdSearchInputField.png")
        self.NyVaccinationSearchField = os.path.join(imagesPath, "Vaccine", "NyVaccinationSearchField.png")
        self.NyAtgardTab = os.path.join(imagesPath, "NyAtgardTab.png")
        self.Covid19AtgardChoice = os.path.join(imagesPath, "Vaccine", "covid19AtgardChoice.png")
        self.VaccinationCovid19Choice = os.path.join(imagesPath, "Vaccine", "VaccinationCovid19Choice.png")
        self.AtgardRelateradCovid19 = os.path.join(imagesPath, "Vaccine", "AtgardRelateradCovid19.png")
        self.CitrixIcon = os.path.join(imagesPath, "CitrixIcon.png")
        self.CitrixIcon2 = os.path.join(imagesPath, "CitrixIcon2.png")
        self.LotNrLabel = os.path.join(imagesPath, "Vaccine", "LotNrLabel.png")
        self.LotNrLabel2 = os.path.join(imagesPath, "Vaccine", "LotNrLabel2.png")
        self.LotNrLabel3 = os.path.join(imagesPath, "Vaccine", "LotNrLabel3.png")
        self.LotNrLabel4 = os.path.join(imagesPath, "Vaccine", "LotNrLabel4.png")
        
        self.DosNummerInputField = os.path.join(imagesPath, "Vaccine", "DosNummerInputField.png")
        self.DosNummerInputField2 = os.path.join(imagesPath, "Vaccine", "DosNummerInputField2.png")
        self.KontraindikationNejCheckbox = os.path.join(imagesPath, "Vaccine", "KontraindikationNejCheckbox.png")
        self.NyVardkontaktTitle = os.path.join(imagesPath, "NyVardkontaktTitle.png")
        self.Covid19VaccinationPatientCheckbox = os.path.join(imagesPath, "Vaccine", "Covid19VaccinationPatientCheckbox.png")
        self.VaccinationsmottagningCheckbox = os.path.join(imagesPath, "Vaccine", "VaccinationsmottagningCheckbox.png")
        self.NyDiagnosTitle = os.path.join(imagesPath, "NyDiagnosTitle.png")
        self.NyAtgardTitle = os.path.join(imagesPath, "NyAtgardTitle.png")
        self.NyVaccinationTab = os.path.join(imagesPath, "NyVaccinationTab.png")
        self.SigneraDisabeledMenu = os.path.join(imagesPath, "SigneraDisabeledMenu.png")
        self.SokTabIcdSearch = os.path.join(imagesPath, "SokTabIcdSearch.png")
        
        self.VaccinationerAtgardChoice = os.path.join(imagesPath, "Vaccine", "VaccinationerAtgardChoice.png")
        self.InfluensasAtgardChoice = os.path.join(imagesPath, "Vaccine", "InfluensasAtgardChoice.png")
        self.InfluensaPneumokockerAtgardChoice = os.path.join(imagesPath, "Vaccine", "InfluensaPneumokockerAtgardChoice.png")
        self.NyVaccinationButton = os.path.join(imagesPath, "Vaccine", "NyVaccinationButton.png")
        self.LokalisationLabel =  os.path.join(imagesPath, "Vaccine", "LokalisationLabel.png")
        self.LokalisationLabel2 = os.path.join(imagesPath, "Vaccine", "LokalisationLabel2.png")
        self.VaccinationLeftMenuItem = os.path.join(imagesPath, "Vaccine", "VaccinationLeftMenuItem.png")
        self.NyVaccinationTitle = os.path.join(imagesPath, "NyVaccinationTitle.png")
        self.Covid19VaccinationPafyllnad_Checkbox  = os.path.join(imagesPath, "Vaccine", "Covid19VaccinationPafyllnad_Checkbox.png")
        self.IdagKnappFranDatumvaljare  = os.path.join(imagesPath, "Vaccine", "IdagKnappFranDatumvaljare.png")

        self.InternpostSymbol = os.path.join(imagesPath, "InternpostSymbol.png")

IMG = ImgsEnum(os.path.join("..", "Images"))

def OpenPMO():
    return waitAndClickOneOf([IMG.CitrixIcon, IMG.CitrixIcon2])


def SignOrSave():
    foundIt = waitForElement(IMG.SigneraDisabeledMenu, limit=0.2, warn=False)
    if not foundIt:
        waitAndPress("alt", "g")
    else:
        waitAndPress("alt", "s")



def OpenPatient():
    
    pos = waitAndClickElement(IMG.IdagKnappFranDatumvaljare, limit=0.5, warn=False)
    
    if pos:
        waitAndPress("enter")
    else:
        pos = waitAndClickElement(IMG.ArbetsflodeLabel, relY=18, conf=0.8)
        if pos:
            waitAndType("covid")
            waitAndPress("enter")
            waitAndPress("enter")
        
    timer = 0

    readyPos = False
    while timer < 15 and not readyPos:
        readyPos = waitForElement(IMG.NyVaccinationSearchField, limit=2, warn=False)
        if not readyPos:
            closePos = waitAndClickElement(IMG.StangButtonText, limit=0.2, warn=False)
            if closePos:
                waitAndClickElement(IMG.StangButtonText, beforeStart=0.5, limit=0.2, warn=False)
    
    return pos


def RegisterVisit(tasks, booster = False):
    waitAndPress("ctrl", "e")
    pos = waitForElement(IMG.NyVardkontaktTitle)
    if pos:
        sleep(0.3)
        waitAndType("m")
    
    if "covid" in tasks:
        if pos:
            pos = waitAndClickElement(IMG.Covid19VaccinationPatientCheckbox, relX=-81)
#         if pos and booster:
#             pos = waitAndClickElement(IMG.Covid19VaccinationPafyllnad_Checkbox, relX=-104)
    if pos:
        pos = waitAndClickElement(IMG.VaccinationsmottagningCheckbox, relX=-71)
        
    if pos:
        SignOrSave()
    if pos:
        pos = waitForElementDisappear(IMG.NyVardkontaktTitle)
        
    return pos


def HandleInternalMail():
    pos = waitForElement(IMG.InternpostSymbol, limit=0.1, waitTime=0.9, warn=False)
    if pos:
        print("Pressing alt+o")
        waitAndPress("alt", "o")
    return pos