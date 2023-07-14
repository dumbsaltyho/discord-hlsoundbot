import sox
import os

class BotErrorGeneric(Exception):
    """ generic bot error, don't use """
    pass

class BotErrorTooManyArgs(Exception):
    """ too many arguments were passed into the list, ie. user did not correctly specify ttsType """
    pass

class BotErrorTtsTypeDoesNotExist(Exception):
    """ ttsType / fileLocation does not exist """
    pass

class HlSoundGen():
    def soundBuilder(ttsType: str, message: str):
        validTtsTypes: list = ['UI', 'agrunt', 'ambience', 'apache', 'aslave', 'barnacle', 'barney', 'boid', 'bullchicken', 'buttons', 'common', 'controller', 'debris', 'doors', 'fans', 'fvox', 'garg', 'gman', 'gonarch', 'hassault', 'headcrab', 'hgrunt', 'holo', 'hornet', 'houndeye', 'ichy', 'items', 'leech', 'misc', 'm', 'mixed', 'nihilanth', 'plats', 'player', 'roach', 'scientist', 'squeek', 'tentacle', 'tride', 'turret', 'voice', 'vox', 'weapons', 'x', 'zombie']
        pwd = os.getcwd()
        messageToList: list = message.split(" ")
        messageAndTypeToList: list = []
        textToSpeech: list = []
        combinedFileName: list = []

        if (not ttsType == "mixed") & (not ttsType == "m"):
            for idx, word in enumerate(messageToList): messageToList[idx] = f"{ttsType}:{word}"

        for word in messageToList: messageAndTypeToList.append(word.split(":"))

        if len(messageAndTypeToList[0]) >= 3:
            if messageAndTypeToList[0][0] == messageAndTypeToList[0][1]:
                for idx, word in enumerate(messageAndTypeToList): messageAndTypeToList[idx].pop(0)
            else:
                raise BotErrorTooManyArgs()

        for idx, word in enumerate(messageAndTypeToList):       
            if not messageAndTypeToList[idx][0] in validTtsTypes: raise BotErrorTtsTypeDoesNotExist()

        if len(messageAndTypeToList) < 2:
            soundFileLocation: str = messageAndTypeToList[0][0]
            soundFileName: str = messageAndTypeToList[0][1]
            generatedSound: str = f"{soundFileLocation}/{soundFileName}.wav"
        else:
            for idx, word in enumerate(messageAndTypeToList):
                soundFileLocation: str = messageAndTypeToList[idx][0]
                soundFileName: str = messageAndTypeToList[idx][1]
                textToSpeech.append(f"{soundFileLocation}/{soundFileName}.wav")
                combinedFileName.append(soundFileName)
            combinedFileName: str = '_'.join(combinedFileName)
            generatedSound: str  = f"voice/{combinedFileName}.wav"
            sox.Combiner().build(textToSpeech, generatedSound, "concatenate")
        return generatedSound